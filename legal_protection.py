"""
Legal Protection System for AI CEO Platform
Handles Terms of Service, user approval flows, and liability protection
"""

import os
import json
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from flask_login import login_required, current_user
from models import db, Tenant, AuditLog
from functools import wraps

logger = logging.getLogger(__name__)

legal_bp = Blueprint('legal', __name__)

# Terms of Service and Legal Agreements
TERMS_OF_SERVICE = {
    'version': '1.0',
    'effective_date': '2025-08-30',
    'content': {
        'liability': {
            'title': 'AI-Generated Content Liability',
            'text': 'User acknowledges that AI CEO generates content, products, and marketing materials automatically. User is solely responsible for reviewing, approving, and ensuring compliance of all AI-generated content before publication. AI CEO platform disclaims liability for content accuracy, legal compliance, or business outcomes.'
        },
        'automation': {
            'title': 'Automated Business Operations',
            'text': 'AI CEO operates autonomously to manage connected accounts, create content, launch products, and run advertising campaigns. User grants permission for these automated actions and maintains full responsibility for business decisions and outcomes.'
        },
        'revenue_sharing': {
            'title': 'Revenue and Fee Structure',
            'text': 'Platform retains 5-10% of gross revenue processed through connected payment systems. Users retain 90-95% of revenue. Platform fees are automatically deducted from transactions. Users responsible for all taxes and legal obligations related to their revenue.'
        },
        'data_usage': {
            'title': 'Data and Privacy',
            'text': 'Platform securely stores OAuth tokens and business data using industry-standard encryption. Data is used solely for providing AI CEO services. Users can revoke access and delete data at any time.'
        },
        'compliance': {
            'title': 'Legal Compliance',
            'text': 'Users must ensure their business activities comply with all applicable laws, regulations, and platform policies. Users are responsible for obtaining necessary licenses, permits, and legal approvals for their business operations.'
        }
    }
}

def require_legal_acceptance(f):
    """Decorator to require legal terms acceptance"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        
        # Check if user has accepted current terms
        tenant = Tenant.query.filter_by(owner_user_id=current_user.id).first()
        if not tenant or not tenant.legal_accepted or tenant.legal_version != TERMS_OF_SERVICE['version']:
            return redirect(url_for('legal.accept_terms'))
        
        return f(*args, **kwargs)
    return decorated_function

def require_action_approval(action_type, description):
    """Decorator to require explicit user approval for AI actions"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if this action type needs approval
            approval_key = f"approval_{action_type}_{current_user.id}"
            
            if not session.get(approval_key):
                # Store the original request details
                session['pending_action'] = {
                    'function': f.__name__,
                    'args': args,
                    'kwargs': kwargs,
                    'action_type': action_type,
                    'description': description
                }
                return redirect(url_for('legal.request_approval', action_type=action_type))
            
            # Remove approval from session (one-time use)
            session.pop(approval_key, None)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

class LegalManager:
    """Manages legal compliance and user approvals"""
    
    def record_acceptance(self, user_id, document_type, version):
        """Record user's acceptance of legal documents"""
        try:
            tenant = Tenant.query.filter_by(owner_user_id=user_id).first()
            if not tenant:
                from oauth_connect import oauth_manager
                tenant = oauth_manager.get_tenant_or_create(user_id)
            
            # Update legal acceptance
            tenant.legal_accepted = True
            tenant.legal_version = version
            tenant.legal_accepted_at = datetime.utcnow()
            db.session.commit()
            
            # Log the acceptance
            audit_log = AuditLog(
                tenant_id=tenant.id,
                actor='user',
                action=f'legal_acceptance_{document_type}',
                payload_json=json.dumps({
                    'document_type': document_type,
                    'version': version,
                    'ip_address': request.environ.get('REMOTE_ADDR'),
                    'user_agent': request.environ.get('HTTP_USER_AGENT')
                }),
                ip_address=request.environ.get('REMOTE_ADDR'),
                user_agent=request.environ.get('HTTP_USER_AGENT')
            )
            db.session.add(audit_log)
            db.session.commit()
            
            logger.info(f"✅ Legal acceptance recorded for user {user_id}: {document_type} v{version}")
            return True
            
        except Exception as e:
            logger.error(f"Legal acceptance recording failed: {e}")
            db.session.rollback()
            return False
    
    def record_action_approval(self, user_id, action_type, approved):
        """Record user's approval/denial of AI actions"""
        try:
            tenant = Tenant.query.filter_by(owner_user_id=user_id).first()
            
            audit_log = AuditLog(
                tenant_id=tenant.id if tenant else None,
                actor='user',
                action=f'action_approval_{action_type}',
                payload_json=json.dumps({
                    'action_type': action_type,
                    'approved': approved,
                    'timestamp': datetime.utcnow().isoformat()
                }),
                ip_address=request.environ.get('REMOTE_ADDR'),
                user_agent=request.environ.get('HTTP_USER_AGENT')
            )
            db.session.add(audit_log)
            db.session.commit()
            
            logger.info(f"✅ Action approval recorded for user {user_id}: {action_type} = {approved}")
            return True
            
        except Exception as e:
            logger.error(f"Action approval recording failed: {e}")
            db.session.rollback()
            return False
    
    def get_user_approvals(self, user_id):
        """Get user's approval history"""
        try:
            tenant = Tenant.query.filter_by(owner_user_id=user_id).first()
            if not tenant:
                return []
            
            approvals = AuditLog.query.filter(
                AuditLog.tenant_id == tenant.id,
                AuditLog.action.like('action_approval_%')
            ).order_by(AuditLog.created_at.desc()).limit(50).all()
            
            return [{
                'action_type': log.action.replace('action_approval_', ''),
                'approved': json.loads(log.payload_json).get('approved'),
                'timestamp': log.created_at.isoformat()
            } for log in approvals]
            
        except Exception as e:
            logger.error(f"Getting user approvals failed: {e}")
            return []

# Initialize manager
legal_manager = LegalManager()

# Routes
@legal_bp.route('/terms')
def terms_of_service():
    """Display Terms of Service"""
    return render_template('terms_of_service.html', terms=TERMS_OF_SERVICE)

@legal_bp.route('/accept-terms', methods=['GET', 'POST'])
@login_required
def accept_terms():
    """Terms acceptance page"""
    if request.method == 'POST':
        try:
            accepted = request.form.get('accept_terms') == 'on'
            
            if not accepted:
                return render_template('accept_terms.html', 
                                     terms=TERMS_OF_SERVICE,
                                     error="You must accept the terms to continue")
            
            success = legal_manager.record_acceptance(
                current_user.id,
                'terms_of_service',
                TERMS_OF_SERVICE['version']
            )
            
            if success:
                # Redirect to original destination or dashboard
                next_page = session.pop('next_page', url_for('dashboard'))
                return redirect(next_page)
            else:
                return render_template('accept_terms.html',
                                     terms=TERMS_OF_SERVICE,
                                     error="Failed to record acceptance")
                
        except Exception as e:
            logger.error(f"Terms acceptance failed: {e}")
            return render_template('accept_terms.html',
                                 terms=TERMS_OF_SERVICE,
                                 error="System error occurred")
    
    return render_template('accept_terms.html', terms=TERMS_OF_SERVICE)

@legal_bp.route('/request-approval/<action_type>')
@login_required
def request_approval(action_type):
    """Request user approval for AI actions"""
    try:
        pending_action = session.get('pending_action')
        if not pending_action:
            return redirect(url_for('dashboard'))
        
        action_descriptions = {
            'publish_content': 'AI CEO wants to publish content to your social media accounts',
            'launch_ads': 'AI CEO wants to launch advertising campaigns with your budget',
            'create_products': 'AI CEO wants to create and list new products in your store',
            'modify_store': 'AI CEO wants to modify your store design or settings',
            'send_emails': 'AI CEO wants to send marketing emails to your customer list'
        }
        
        description = action_descriptions.get(action_type, pending_action.get('description', 'AI CEO wants to perform an automated action'))
        
        return render_template('request_approval.html',
                             action_type=action_type,
                             description=description,
                             pending_action=pending_action)
        
    except Exception as e:
        logger.error(f"Approval request failed: {e}")
        return redirect(url_for('dashboard'))

@legal_bp.route('/approve-action', methods=['POST'])
@login_required
def approve_action():
    """Process user's action approval"""
    try:
        action_type = request.form.get('action_type')
        approved = request.form.get('approval') == 'approve'
        
        # Record the approval
        legal_manager.record_action_approval(current_user.id, action_type, approved)
        
        if approved:
            # Grant approval in session
            approval_key = f"approval_{action_type}_{current_user.id}"
            session[approval_key] = True
            
            # Execute the pending action
            pending_action = session.pop('pending_action', None)
            if pending_action:
                return redirect(url_for('dashboard'))  # Would redirect to original action
        
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        logger.error(f"Action approval processing failed: {e}")
        return redirect(url_for('dashboard'))

@legal_bp.route('/privacy-policy')
def privacy_policy():
    """Display Privacy Policy"""
    privacy_policy = {
        'effective_date': '2025-08-30',
        'sections': {
            'data_collection': {
                'title': 'Data We Collect',
                'content': 'We collect OAuth tokens, business metrics, and usage data necessary to provide AI CEO services. All data is encrypted and stored securely.'
            },
            'data_usage': {
                'title': 'How We Use Data',
                'content': 'Data is used exclusively to provide AI CEO automation services including content generation, business management, and analytics. We do not sell or share personal data.'
            },
            'data_retention': {
                'title': 'Data Retention',
                'content': 'Data is retained while your account is active. You can request data deletion at any time. OAuth tokens are immediately revoked when you disconnect platforms.'
            },
            'security': {
                'title': 'Security Measures',
                'content': 'We use industry-standard encryption (Fernet), secure token storage, and audit logging to protect your data and business information.'
            }
        }
    }
    return render_template('privacy_policy.html', policy=privacy_policy)

@legal_bp.route('/api/legal/compliance-status')
@login_required
def compliance_status():
    """Get user's legal compliance status"""
    try:
        tenant = Tenant.query.filter_by(owner_user_id=current_user.id).first()
        
        status = {
            'terms_accepted': False,
            'terms_version': None,
            'accepted_date': None,
            'compliance_score': 0
        }
        
        if tenant:
            status.update({
                'terms_accepted': tenant.legal_accepted or False,
                'terms_version': tenant.legal_version,
                'accepted_date': tenant.legal_accepted_at.isoformat() if tenant.legal_accepted_at else None,
                'compliance_score': 100 if tenant.legal_accepted else 0
            })
        
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Compliance status check failed: {e}")
        return jsonify({'error': str(e)}), 500

@legal_bp.route('/api/legal/audit-log')
@login_required
def get_audit_log():
    """Get user's audit log for transparency"""
    try:
        tenant = Tenant.query.filter_by(owner_user_id=current_user.id).first()
        if not tenant:
            return jsonify([])
        
        # Get recent audit logs
        logs = AuditLog.query.filter_by(tenant_id=tenant.id)\
                           .order_by(AuditLog.created_at.desc())\
                           .limit(100).all()
        
        audit_data = []
        for log in logs:
            audit_data.append({
                'timestamp': log.created_at.isoformat(),
                'actor': log.actor,
                'action': log.action,
                'payload': json.loads(log.payload_json) if log.payload_json else {},
                'ip_address': log.ip_address
            })
        
        return jsonify(audit_data)
        
    except Exception as e:
        logger.error(f"Audit log retrieval failed: {e}")
        return jsonify({'error': str(e)}), 500