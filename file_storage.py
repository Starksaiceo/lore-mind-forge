
import os
import uuid
import mimetypes
from datetime import datetime
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class FileStorageManager:
    """Comprehensive file storage system for AI CEO platform"""
    
    def __init__(self):
        self.setup_storage()
    
    def setup_storage(self):
        """Initialize storage backends"""
        try:
            # Try to use Replit Object Storage for cloud storage
            from replit.object_storage import Client
            self.cloud_client = Client()
            self.cloud_enabled = True
            logger.info("✅ Cloud storage (Replit Object Storage) initialized")
        except ImportError:
            logger.warning("⚠️ Replit Object Storage not available, using local storage")
            self.cloud_enabled = False
            self.cloud_client = None
        
        # Ensure local directories exist
        self.local_dirs = {
            'media': 'static/media',
            'uploads': 'uploads',
            'content': 'generated_content',
            'backups': 'backups',
            'downloads': 'downloads'
        }
        
        for dir_path in self.local_dirs.values():
            os.makedirs(dir_path, exist_ok=True)
    
    def upload_media(self, file_data: bytes, filename: str, user_id: int, 
                    content_type: str = None) -> Dict[str, Any]:
        """Upload media files (images, videos) with cloud storage and CDN"""
        try:
            # Generate unique filename
            file_ext = os.path.splitext(filename)[1]
            unique_filename = f"user_{user_id}_{uuid.uuid4().hex}{file_ext}"
            
            # Detect content type if not provided
            if not content_type:
                content_type, _ = mimetypes.guess_type(filename)
                content_type = content_type or 'application/octet-stream'
            
            # Upload to cloud storage first (if available)
            cloud_url = None
            if self.cloud_enabled:
                try:
                    cloud_path = f"media/{unique_filename}"
                    self.cloud_client.upload_from_text(cloud_path, file_data.decode('latin-1'))
                    cloud_url = f"/api/media/{cloud_path}"
                    logger.info(f"✅ Media uploaded to cloud: {cloud_path}")
                except Exception as e:
                    logger.error(f"❌ Cloud upload failed: {e}")
            
            # Always save locally as backup
            local_path = os.path.join(self.local_dirs['media'], unique_filename)
            with open(local_path, 'wb') as f:
                f.write(file_data)
            
            # Create CDN-like URL structure
            cdn_url = f"/static/media/{unique_filename}"
            
            return {
                'success': True,
                'filename': unique_filename,
                'original_filename': filename,
                'local_path': local_path,
                'cdn_url': cdn_url,
                'cloud_url': cloud_url,
                'content_type': content_type,
                'size': len(file_data),
                'user_id': user_id
            }
            
        except Exception as e:
            logger.error(f"❌ Media upload failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def upload_content(self, content: str, filename: str, user_id: int, 
                      content_type: str = 'text/plain') -> Dict[str, Any]:
        """Upload generated content with backup"""
        try:
            # Generate unique filename for content
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"user_{user_id}_{timestamp}_{filename}"
            
            # Upload to cloud storage
            cloud_url = None
            if self.cloud_enabled:
                try:
                    cloud_path = f"content/{unique_filename}"
                    self.cloud_client.upload_from_text(cloud_path, content)
                    cloud_url = f"/api/content/{cloud_path}"
                    logger.info(f"✅ Content uploaded to cloud: {cloud_path}")
                except Exception as e:
                    logger.error(f"❌ Cloud content upload failed: {e}")
            
            # Save locally
            local_path = os.path.join(self.local_dirs['content'], unique_filename)
            with open(local_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Create backup
            self.create_backup(unique_filename, content, user_id)
            
            return {
                'success': True,
                'filename': unique_filename,
                'local_path': local_path,
                'cloud_url': cloud_url,
                'download_url': f"/download/{unique_filename}",
                'content_type': content_type,
                'size': len(content.encode('utf-8')),
                'user_id': user_id
            }
            
        except Exception as e:
            logger.error(f"❌ Content upload failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def create_backup(self, filename: str, content: str, user_id: int):
        """Create backup of generated content"""
        try:
            backup_dir = os.path.join(self.local_dirs['backups'], f"user_{user_id}")
            os.makedirs(backup_dir, exist_ok=True)
            
            backup_path = os.path.join(backup_dir, filename)
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ Backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"❌ Backup creation failed: {e}")
            return None
    
    def get_file(self, filename: str, user_id: int = None) -> Optional[Dict[str, Any]]:
        """Retrieve file from storage"""
        try:
            # Try cloud storage first
            if self.cloud_enabled:
                try:
                    content = self.cloud_client.download_as_text(f"content/{filename}")
                    return {
                        'success': True,
                        'content': content,
                        'source': 'cloud',
                        'filename': filename
                    }
                except Exception as e:
                    logger.warning(f"Cloud retrieval failed: {e}")
            
            # Fallback to local storage
            for dir_name, dir_path in self.local_dirs.items():
                file_path = os.path.join(dir_path, filename)
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return {
                        'success': True,
                        'content': content,
                        'source': 'local',
                        'filename': filename,
                        'path': file_path
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"❌ File retrieval failed: {e}")
            return None
    
    def list_user_files(self, user_id: int, file_type: str = 'all') -> List[Dict[str, Any]]:
        """List all files for a user"""
        try:
            files = []
            
            # Check cloud storage
            if self.cloud_enabled:
                try:
                    cloud_objects = self.cloud_client.list()
                    for obj in cloud_objects:
                        if f"user_{user_id}" in obj.name:
                            files.append({
                                'filename': obj.name,
                                'source': 'cloud',
                                'type': 'cloud_object'
                            })
                except Exception as e:
                    logger.warning(f"Cloud listing failed: {e}")
            
            # Check local storage
            if file_type in ['all', 'content']:
                content_dir = self.local_dirs['content']
                for filename in os.listdir(content_dir):
                    if f"user_{user_id}" in filename:
                        file_path = os.path.join(content_dir, filename)
                        stat = os.stat(file_path)
                        files.append({
                            'filename': filename,
                            'source': 'local',
                            'type': 'content',
                            'size': stat.st_size,
                            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                        })
            
            if file_type in ['all', 'media']:
                media_dir = self.local_dirs['media']
                for filename in os.listdir(media_dir):
                    if f"user_{user_id}" in filename:
                        file_path = os.path.join(media_dir, filename)
                        stat = os.stat(file_path)
                        files.append({
                            'filename': filename,
                            'source': 'local',
                            'type': 'media',
                            'size': stat.st_size,
                            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            'url': f"/static/media/{filename}"
                        })
            
            return files
            
        except Exception as e:
            logger.error(f"❌ File listing failed: {e}")
            return []
    
    def delete_file(self, filename: str, user_id: int) -> bool:
        """Delete file from all storage locations"""
        try:
            deleted = False
            
            # Delete from cloud
            if self.cloud_enabled:
                try:
                    self.cloud_client.delete(filename)
                    deleted = True
                    logger.info(f"✅ Deleted from cloud: {filename}")
                except Exception as e:
                    logger.warning(f"Cloud deletion failed: {e}")
            
            # Delete from local storage
            for dir_path in self.local_dirs.values():
                file_path = os.path.join(dir_path, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted = True
                    logger.info(f"✅ Deleted locally: {file_path}")
            
            return deleted
            
        except Exception as e:
            logger.error(f"❌ File deletion failed: {e}")
            return False
    
    def get_storage_stats(self, user_id: int = None) -> Dict[str, Any]:
        """Get storage statistics"""
        try:
            stats = {
                'cloud_enabled': self.cloud_enabled,
                'total_files': 0,
                'total_size': 0,
                'by_type': {},
                'by_user': {}
            }
            
            # Count local files
            for dir_name, dir_path in self.local_dirs.items():
                if os.path.exists(dir_path):
                    files = os.listdir(dir_path)
                    if user_id:
                        files = [f for f in files if f"user_{user_id}" in f]
                    
                    type_size = 0
                    for filename in files:
                        file_path = os.path.join(dir_path, filename)
                        if os.path.isfile(file_path):
                            size = os.path.getsize(file_path)
                            type_size += size
                            stats['total_size'] += size
                            stats['total_files'] += 1
                    
                    stats['by_type'][dir_name] = {
                        'files': len(files),
                        'size': type_size
                    }
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Stats calculation failed: {e}")
            return {'error': str(e)}

# Global instance
file_storage = FileStorageManager()
