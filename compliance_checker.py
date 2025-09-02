
import re
from typing import Dict, List, Optional

class ComplianceChecker:
    def __init__(self):
        self.compliance_rules = {
            "title_length": {"min": 10, "max": 100},
            "description_length": {"min": 50, "max": 2000},
            "price_range": {"min": 5.0, "max": 500.0},
            "prohibited_words": ["guaranteed money", "get rich quick", "no work required"],
            "required_disclaimers": ["results may vary", "for educational purposes"]
        }
        
    def get_compliance_score(self, product_data: Dict) -> Dict:
        """Calculate compliance score for a product"""
        try:
            title = product_data.get("title", "")
            description = product_data.get("description", "")
            price = product_data.get("price", 0.0)
            
            score = 100
            issues = []
            warnings = []
            
            # Check title compliance
            title_check = self._check_title_compliance(title)
            score -= title_check["penalty"]
            issues.extend(title_check["issues"])
            warnings.extend(title_check["warnings"])
            
            # Check description compliance
            desc_check = self._check_description_compliance(description)
            score -= desc_check["penalty"]
            issues.extend(desc_check["issues"])
            warnings.extend(desc_check["warnings"])
            
            # Check price compliance
            price_check = self._check_price_compliance(price)
            score -= price_check["penalty"]
            issues.extend(price_check["issues"])
            warnings.extend(price_check["warnings"])
            
            # Determine grade and status
            grade, status = self._calculate_grade_status(score)
            
            return {
                "success": True,
                "compliance_score": max(score, 0),
                "grade": grade,
                "status": status,
                "issues": issues,
                "warnings": warnings,
                "recommendations": self._generate_recommendations(issues, warnings)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _check_title_compliance(self, title: str) -> Dict:
        """Check title compliance"""
        penalty = 0
        issues = []
        warnings = []
        
        # Length check
        if len(title) < self.compliance_rules["title_length"]["min"]:
            penalty += 15
            issues.append(f"Title too short (min {self.compliance_rules['title_length']['min']} chars)")
        elif len(title) > self.compliance_rules["title_length"]["max"]:
            penalty += 10
            warnings.append(f"Title may be too long (max {self.compliance_rules['title_length']['max']} chars recommended)")
        
        # Prohibited words check
        for word in self.compliance_rules["prohibited_words"]:
            if word.lower() in title.lower():
                penalty += 25
                issues.append(f"Contains prohibited phrase: '{word}'")
        
        # Professional language check
        if re.search(r'[!]{3,}', title):  # Multiple exclamation marks
            penalty += 5
            warnings.append("Excessive punctuation detected")
        
        return {"penalty": penalty, "issues": issues, "warnings": warnings}
    
    def _check_description_compliance(self, description: str) -> Dict:
        """Check description compliance"""
        penalty = 0
        issues = []
        warnings = []
        
        # Length check
        if len(description) < self.compliance_rules["description_length"]["min"]:
            penalty += 20
            issues.append(f"Description too short (min {self.compliance_rules['description_length']['min']} chars)")
        elif len(description) > self.compliance_rules["description_length"]["max"]:
            penalty += 5
            warnings.append(f"Description very long (may affect readability)")
        
        # Prohibited words check
        for word in self.compliance_rules["prohibited_words"]:
            if word.lower() in description.lower():
                penalty += 30
                issues.append(f"Contains prohibited phrase: '{word}'")
        
        # Disclaimer check
        has_disclaimer = any(disclaimer in description.lower() 
                           for disclaimer in self.compliance_rules["required_disclaimers"])
        if not has_disclaimer:
            penalty += 10
            warnings.append("Consider adding appropriate disclaimers")
        
        # Professional tone check
        spam_indicators = ["!!!!", "100% guaranteed", "AMAZING DEAL", "MUST BUY NOW"]
        for indicator in spam_indicators:
            if indicator.lower() in description.lower():
                penalty += 15
                warnings.append(f"Potentially spammy language: '{indicator}'")
        
        return {"penalty": penalty, "issues": issues, "warnings": warnings}
    
    def _check_price_compliance(self, price: float) -> Dict:
        """Check price compliance"""
        penalty = 0
        issues = []
        warnings = []
        
        # Price range check
        if price < self.compliance_rules["price_range"]["min"]:
            penalty += 20
            issues.append(f"Price too low (min ${self.compliance_rules['price_range']['min']})")
        elif price > self.compliance_rules["price_range"]["max"]:
            penalty += 15
            warnings.append(f"High price may require additional justification")
        
        # Psychological pricing check
        if price == int(price):  # Whole number pricing
            warnings.append("Consider charm pricing (e.g., $47 instead of $47.00)")
        
        return {"penalty": penalty, "issues": issues, "warnings": warnings}
    
    def _calculate_grade_status(self, score: int) -> tuple:
        """Calculate grade and status based on score"""
        if score >= 90:
            return "A", "Excellent - Ready to launch"
        elif score >= 80:
            return "B", "Good - Minor improvements recommended"
        elif score >= 70:
            return "C", "Acceptable - Some issues to address"
        elif score >= 60:
            return "D", "Needs improvement - Several issues found"
        else:
            return "F", "Major issues - Requires significant changes"
    
    def _generate_recommendations(self, issues: List[str], warnings: List[str]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if issues:
            recommendations.append("Address critical compliance issues first")
        
        if warnings:
            recommendations.append("Review warnings to improve product quality")
        
        if not issues and not warnings:
            recommendations = [
                "Product meets compliance standards",
                "Consider A/B testing different variations",
                "Monitor performance after launch"
            ]
        else:
            recommendations.extend([
                "Review product against platform guidelines",
                "Consider professional copywriting review",
                "Test with target audience before launch"
            ])
        
        return recommendations
    
    def check_platform_compliance(self, product_data: Dict, platform: str) -> Dict:
        """Check compliance for specific platform"""
        try:
            base_compliance = self.get_compliance_score(product_data)
            
            # Platform-specific rules
            platform_rules = {
                "shopify": {
                    "max_title_length": 70,
                    "required_fields": ["title", "description", "price"],
                    "image_required": True
                },
                "stripe": {
                    "max_description_length": 1000,
                    "requires_tax_info": True,
                    "subscription_allowed": True
                }
            }
            
            if platform in platform_rules:
                rules = platform_rules[platform]
                additional_checks = self._platform_specific_checks(product_data, rules)
                
                # Merge results
                base_compliance["platform_specific"] = additional_checks
                if additional_checks.get("issues"):
                    base_compliance["compliance_score"] -= 10
                    base_compliance["issues"].extend(additional_checks["issues"])
            
            return base_compliance
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _platform_specific_checks(self, product_data: Dict, rules: Dict) -> Dict:
        """Perform platform-specific compliance checks"""
        issues = []
        warnings = []
        
        # Check required fields
        for field in rules.get("required_fields", []):
            if not product_data.get(field):
                issues.append(f"Missing required field: {field}")
        
        # Check title length for platform
        if "max_title_length" in rules:
            title = product_data.get("title", "")
            if len(title) > rules["max_title_length"]:
                warnings.append(f"Title exceeds platform limit of {rules['max_title_length']} characters")
        
        return {"issues": issues, "warnings": warnings}
