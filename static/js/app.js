// AI CEO SaaS - Modern JavaScript Framework

class AICEOApp {
  constructor() {
    this.theme = localStorage.getItem('theme') || 'light';
    this.init();
  }

  init() {
    this.setupTheme();
    this.setupAnimations();
    this.setupCounters();
    this.setupProgressBars();
    this.setupCharts();
    this.setupNotifications();
    this.bindEvents();
  }

  // Theme Management
  setupTheme() {
    document.body.classList.toggle('dark', this.theme === 'dark');
    this.updateThemeIcon();
  }

  toggleTheme() {
    this.theme = this.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', this.theme);
    document.body.classList.toggle('dark', this.theme === 'dark');
    this.updateThemeIcon();
  }

  updateThemeIcon() {
    const icon = document.querySelector('.theme-toggle-icon');
    if (icon) {
      icon.innerHTML = this.theme === 'light' 
        ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>'
        : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><path d="m12 1-3 6-3-6"></path><path d="m21 4-6 6-6-6"></path><path d="m21 20-6-6 6-6"></path><path d="m3 20 6-6-6-6"></path></svg>';
    }
  }

  // Animation System
  setupAnimations() {
    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-fadeIn');
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });

    // Observe all cards and main content sections
    document.querySelectorAll('.card, .kpi-card, .hero-section').forEach(el => {
      observer.observe(el);
    });
  }

  // Animated Counters
  setupCounters() {
    const counters = document.querySelectorAll('.kpi-value[data-count]');
    
    counters.forEach(counter => {
      const target = parseInt(counter.dataset.count);
      const duration = 2000; // 2 seconds
      const increment = target / (duration / 16); // 60 FPS
      let current = 0;

      const updateCounter = () => {
        if (current < target) {
          current += increment;
          counter.textContent = this.formatNumber(Math.ceil(current));
          requestAnimationFrame(updateCounter);
        } else {
          counter.textContent = this.formatNumber(target);
        }
      };

      // Start animation when element is visible
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            updateCounter();
            observer.unobserve(entry.target);
          }
        });
      });

      observer.observe(counter);
    });
  }

  // Progress Bar Animations
  setupProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar[data-progress]');
    
    progressBars.forEach(bar => {
      const progress = parseInt(bar.dataset.progress);
      
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            setTimeout(() => {
              bar.style.width = progress + '%';
            }, 500);
            observer.unobserve(entry.target);
          }
        });
      });

      observer.observe(bar);
    });
  }

  // Chart Setup (Chart.js integration)
  setupCharts() {
    // Revenue Chart
    const revenueCtx = document.getElementById('revenueChart');
    if (revenueCtx && typeof Chart !== 'undefined') {
      new Chart(revenueCtx, {
        type: 'line',
        data: {
          labels: this.getLast30Days(),
          datasets: [{
            label: 'Revenue ($)',
            data: this.generateSampleData(30),
            borderColor: getComputedStyle(document.documentElement).getPropertyValue('--primary'),
            backgroundColor: getComputedStyle(document.documentElement).getPropertyValue('--primary') + '20',
            borderWidth: 3,
            fill: true,
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0,0,0,0.1)'
              }
            },
            x: {
              grid: {
                display: false
              }
            }
          },
          elements: {
            point: {
              radius: 0,
              hoverRadius: 6
            }
          }
        }
      });
    }

    // Orders vs Ad Spend Chart
    const ordersCtx = document.getElementById('ordersChart');
    if (ordersCtx && typeof Chart !== 'undefined') {
      new Chart(ordersCtx, {
        type: 'bar',
        data: {
          labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
          datasets: [{
            label: 'Orders',
            data: [12, 19, 15, 25],
            backgroundColor: getComputedStyle(document.documentElement).getPropertyValue('--accent'),
            borderRadius: 6
          }, {
            label: 'Ad Spend',
            data: [8, 15, 12, 20],
            backgroundColor: getComputedStyle(document.documentElement).getPropertyValue('--primary'),
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom'
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }
  }

  // Notification System
  setupNotifications() {
    // Create notification container if it doesn't exist
    if (!document.getElementById('notification-container')) {
      const container = document.createElement('div');
      container.id = 'notification-container';
      container.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        display: flex;
        flex-direction: column;
        gap: 10px;
      `;
      document.body.appendChild(container);
    }
  }

  showNotification(message, type = 'info', duration = 5000) {
    const container = document.getElementById('notification-container');
    const notification = document.createElement('div');
    
    const colors = {
      success: 'var(--accent)',
      error: 'var(--error)',
      warning: 'var(--warning)',
      info: 'var(--primary)'
    };

    notification.style.cssText = `
      background: ${colors[type] || colors.info};
      color: white;
      padding: 16px 20px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      transform: translateX(100%);
      transition: transform 0.3s ease;
      max-width: 350px;
      word-wrap: break-word;
      display: flex;
      align-items: center;
      gap: 10px;
    `;

    notification.innerHTML = `
      <span>${message}</span>
      <button style="background: none; border: none; color: white; cursor: pointer; font-size: 18px; padding: 0; margin-left: auto;">&times;</button>
    `;

    container.appendChild(notification);

    // Animate in
    setTimeout(() => {
      notification.style.transform = 'translateX(0)';
    }, 10);

    // Auto remove
    const removeNotification = () => {
      notification.style.transform = 'translateX(100%)';
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 300);
    };

    // Close button
    notification.querySelector('button').addEventListener('click', removeNotification);

    // Auto remove after duration
    if (duration > 0) {
      setTimeout(removeNotification, duration);
    }
  }

  // Event Binding
  bindEvents() {
    // Theme toggle
    document.addEventListener('click', (e) => {
      if (e.target.closest('.theme-toggle')) {
        this.toggleTheme();
      }
    });

    // Sidebar toggle for mobile
    document.addEventListener('click', (e) => {
      if (e.target.closest('.sidebar-toggle')) {
        document.querySelector('.sidebar').classList.toggle('collapsed');
        document.querySelector('.main-content').classList.toggle('expanded');
      }
    });

    // Form enhancements
    document.querySelectorAll('.form-input').forEach(input => {
      input.addEventListener('focus', () => {
        input.parentNode.classList.add('focused');
      });
      
      input.addEventListener('blur', () => {
        input.parentNode.classList.remove('focused');
      });
    });

    // Button loading states
    document.addEventListener('click', (e) => {
      if (e.target.matches('.btn[data-loading]')) {
        const btn = e.target;
        const originalText = btn.textContent;
        btn.textContent = 'Loading...';
        btn.disabled = true;
        
        // Simulate loading (remove this in real implementation)
        setTimeout(() => {
          btn.textContent = originalText;
          btn.disabled = false;
        }, 2000);
      }
    });

    // Smooth scroll for anchor links
    document.addEventListener('click', (e) => {
      if (e.target.matches('a[href^="#"]')) {
        e.preventDefault();
        const target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  }

  // Utility Functions
  formatNumber(num) {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  }

  formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  }

  getLast30Days() {
    const days = [];
    for (let i = 29; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      days.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
    }
    return days;
  }

  generateSampleData(length) {
    return Array.from({ length }, () => Math.floor(Math.random() * 1000) + 100);
  }

  // API Integration
  async apiCall(endpoint, options = {}) {
    try {
      const response = await fetch(endpoint, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      this.showNotification(`API Error: ${error.message}`, 'error');
      throw error;
    }
  }

  // Real-time Updates
  setupRealTimeUpdates() {
    // Update KPIs every 30 seconds
    setInterval(() => {
      this.updateKPIs();
    }, 30000);

    // Update charts every 5 minutes (only if updateCharts method exists)
    if (typeof this.updateCharts === 'function') {
      setInterval(() => {
        this.updateCharts();
      }, 300000);
    }
  }

  async updateKPIs() {
    try {
      const kpis = await this.apiCall('/api/kpis');
      
      Object.entries(kpis).forEach(([key, value]) => {
        const element = document.querySelector(`[data-kpi="${key}"]`);
        if (element) {
          this.animateKPIUpdate(element, value);
        }
      });
    } catch (error) {
      console.error('Failed to update KPIs:', error);
    }
  }

  animateKPIUpdate(element, newValue) {
    const currentValue = parseInt(element.textContent.replace(/[^0-9]/g, ''));
    const difference = newValue - currentValue;
    
    if (difference !== 0) {
      element.classList.add('animate-pulse');
      setTimeout(() => {
        element.textContent = this.formatNumber(newValue);
        element.classList.remove('animate-pulse');
      }, 500);
    }
  }
}

// White-label Customization
class BrandCustomizer {
  constructor() {
    this.loadBrandSettings();
  }

  loadBrandSettings() {
    // Check if tenant has custom branding
    const brandSettings = window.brandSettings || {};
    
    if (brandSettings.primaryColor) {
      document.documentElement.style.setProperty('--custom-primary', brandSettings.primaryColor);
    }
    
    if (brandSettings.secondaryColor) {
      document.documentElement.style.setProperty('--custom-secondary', brandSettings.secondaryColor);
    }
    
    if (brandSettings.accentColor) {
      document.documentElement.style.setProperty('--custom-accent', brandSettings.accentColor);
    }
    
    if (brandSettings.logo) {
      this.updateLogo(brandSettings.logo);
    }
    
    if (brandSettings.favicon) {
      this.updateFavicon(brandSettings.favicon);
    }
    
    // Apply brand override class
    if (Object.keys(brandSettings).length > 0) {
      document.body.classList.add('brand-override');
    }
  }

  updateLogo(logoUrl) {
    document.querySelectorAll('.brand-logo').forEach(logo => {
      if (logo.tagName === 'IMG') {
        logo.src = logoUrl;
      } else {
        logo.style.backgroundImage = `url(${logoUrl})`;
      }
    });
  }

  updateFavicon(faviconUrl) {
    const favicon = document.querySelector('link[rel="icon"]') || document.createElement('link');
    favicon.rel = 'icon';
    favicon.href = faviconUrl;
    if (!document.querySelector('link[rel="icon"]')) {
      document.head.appendChild(favicon);
    }
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.aiCEOApp = new AICEOApp();
  window.brandCustomizer = new BrandCustomizer();
  
  // Setup real-time updates only on dashboard pages (not homepage)
  if (window.location.pathname !== '/' && !window.location.pathname.includes('index')) {
    window.aiCEOApp.setupRealTimeUpdates();
  }
  
  // Show welcome notification
  setTimeout(() => {
    window.aiCEOApp.showNotification('🚀 Welcome to AI CEO! Your autonomous business platform is ready.', 'success', 8000);
  }, 1000);
});

// Business Creation Modal Functions
function showBuildFromScratchModal() {
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center';
    modal.style.zIndex = '99999';
    modal.innerHTML = `
        <div class="bg-gray-800 rounded-xl p-8 max-w-2xl w-full mx-4 border border-blue-500">
            <div class="flex items-center mb-6">
                <div class="p-3 bg-blue-600 rounded-full mr-4">
                    <i class="fas fa-rocket text-white text-xl"></i>
                </div>
                <h2 class="text-2xl font-bold text-white">🚀 Build Complete Business From Scratch</h2>
            </div>
            
            <div class="space-y-4 mb-6">
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Business Niche/Industry</label>
                    <input type="text" id="businessNiche" placeholder="e.g., Digital Marketing, Fitness, SaaS Tools..." 
                           class="w-full p-3 border border-slate-600 rounded-lg bg-gray-700 text-white placeholder-slate-400">
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Business Name (Optional)</label>
                    <input type="text" id="businessName" placeholder="Leave blank for AI to generate..." 
                           class="w-full p-3 border border-slate-600 rounded-lg bg-gray-700 text-white placeholder-slate-400">
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Target Monthly Revenue</label>
                    <select id="targetRevenue" class="w-full p-3 border border-slate-600 rounded-lg bg-gray-700 text-white">
                        <option value="10000">$10,000/month</option>
                        <option value="25000">$25,000/month</option>
                        <option value="50000">$50,000/month</option>
                        <option value="100000">$100,000/month</option>
                        <option value="250000">$250,000/month</option>
                        <option value="500000">$500,000+/month</option>
                    </select>
                </div>
            </div>
            
            <div class="flex gap-4">
                <button onclick="startBuildingBusiness()" 
                        class="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg font-bold hover:bg-blue-700 transition-colors">
                    🚀 Start Building
                </button>
                <button onclick="closeBuildModal()" 
                        class="px-6 py-3 border border-slate-600 text-slate-300 rounded-lg hover:bg-gray-700 transition-colors">
                    Cancel
                </button>
            </div>
        </div>
    `;
    
    modal.onclick = (e) => {
        if (e.target === modal) closeBuildModal();
    };
    
    document.body.appendChild(modal);
    window.currentModal = modal;
}

function showConnectStoreModal() {
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center';
    modal.style.zIndex = '99999';
    modal.innerHTML = `
        <div class="bg-gray-800 rounded-xl p-8 max-w-2xl w-full mx-4 border border-green-500">
            <div class="flex items-center mb-6">
                <div class="p-3 bg-green-600 rounded-full mr-4">
                    <i class="fas fa-store text-white text-xl"></i>
                </div>
                <h2 class="text-2xl font-bold text-white">🏪 Connect Your Existing Store</h2>
            </div>
            
            <div class="space-y-4 mb-6">
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Store Platform</label>
                    <select id="storePlatform" class="w-full p-3 border border-slate-600 rounded-lg bg-gray-700 text-white">
                        <option value="shopify">Shopify Store</option>
                        <option value="woocommerce">WooCommerce</option>
                        <option value="bigcommerce">BigCommerce</option>
                        <option value="etsy">Etsy Shop</option>
                        <option value="amazon">Amazon FBA</option>
                        <option value="other">Other Platform</option>
                    </select>
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Store URL</label>
                    <input type="url" id="storeUrl" placeholder="https://your-store.com or https://your-store.myshopify.com" 
                           class="w-full p-3 border border-slate-600 rounded-lg bg-gray-700 text-white placeholder-slate-400">
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">Current Monthly Revenue (Optional)</label>
                    <input type="number" id="currentRevenue" placeholder="e.g., 5000" 
                           class="w-full p-3 border border-slate-600 rounded-lg bg-gray-700 text-white placeholder-slate-400">
                </div>
                
                <div class="bg-yellow-900 bg-opacity-30 border border-yellow-600 rounded-lg p-4">
                    <h4 class="text-yellow-300 font-semibold mb-2">⚠️ What Happens Next:</h4>
                    <ul class="text-sm text-yellow-100 space-y-1">
                        <li>• AI will analyze your store and products</li>
                        <li>• Optimize all product descriptions for SEO</li>
                        <li>• Start automated marketing campaigns</li>
                        <li>• Begin social media content creation</li>
                        <li>• Setup revenue tracking and optimization</li>
                    </ul>
                </div>
            </div>
            
            <div class="flex gap-4">
                <button onclick="connectExistingStore()" 
                        class="flex-1 bg-green-600 text-white py-3 px-6 rounded-lg font-bold hover:bg-green-700 transition-colors">
                    🔗 Connect & Optimize
                </button>
                <button onclick="closeConnectModal()" 
                        class="px-6 py-3 border border-slate-600 text-slate-300 rounded-lg hover:bg-gray-700 transition-colors">
                    Cancel
                </button>
            </div>
        </div>
    `;
    
    modal.onclick = (e) => {
        if (e.target === modal) closeConnectModal();
    };
    
    document.body.appendChild(modal);
    window.currentModal = modal;
}

function startBuildingBusiness() {
    const niche = document.getElementById('businessNiche').value;
    const name = document.getElementById('businessName').value;
    const revenue = document.getElementById('targetRevenue').value;
    
    if (!niche.trim()) {
        alert('Please enter a business niche or industry');
        return;
    }
    
    closeBuildModal();
    
    // Show loading indicator
    showNotification('🚀 AI CEO is building your complete business... This may take a few minutes.', 'info', 10000);
    
    // Launch business creation
    fetch('/launch-business', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            niche: niche,
            business_name: name || null,
            target_revenue: parseInt(revenue),
            description: `AI-powered ${niche} business with automated marketing and sales`
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('✅ Business creation started! Check your dashboard for progress.', 'success', 8000);
            // Refresh dashboard data
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            showNotification('❌ Failed to start business creation: ' + (data.error || 'Unknown error'), 'error', 8000);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('❌ Network error while creating business', 'error', 8000);
    });
}

function connectExistingStore() {
    const platform = document.getElementById('storePlatform').value;
    const url = document.getElementById('storeUrl').value;
    const revenue = document.getElementById('currentRevenue').value;
    
    if (!url.trim()) {
        alert('Please enter your store URL');
        return;
    }
    
    closeConnectModal();
    
    // Show loading indicator
    showNotification('🔗 AI CEO is connecting to your store and analyzing optimization opportunities...', 'info', 10000);
    
    // Connect store
    fetch('/api/stores/connect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            platform: platform,
            store_url: url,
            current_revenue: revenue ? parseInt(revenue) : null
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('✅ Store connected! AI CEO is now optimizing your business.', 'success', 8000);
            // Refresh dashboard data
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            showNotification('❌ Failed to connect store: ' + (data.error || 'Unknown error'), 'error', 8000);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('❌ Network error while connecting store', 'error', 8000);
    });
}

function closeBuildModal() {
    if (window.currentModal) {
        document.body.removeChild(window.currentModal);
        window.currentModal = null;
    }
}

function closeConnectModal() {
    console.log('🔍 closeConnectModal called');
    if (window.currentModal) {
        console.log('🔍 Removing modal from DOM');
        document.body.removeChild(window.currentModal);
        window.currentModal = null;
        console.log('✅ Modal closed successfully');
    } else {
        console.log('⚠️ No modal found to close');
    }
}

function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
        type === 'success' ? 'bg-green-600' :
        type === 'error' ? 'bg-red-600' :
        type === 'warning' ? 'bg-yellow-600' :
        'bg-blue-600'
    } text-white max-w-sm`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            document.body.removeChild(notification);
        }
    }, duration);
}

// Export for use in other modules
window.AICEOApp = AICEOApp;
window.BrandCustomizer = BrandCustomizer;

// Export modal functions to global scope
window.showConnectStoreModal = showConnectStoreModal;
window.showBuildFromScratchModal = showBuildFromScratchModal;
window.closeConnectModal = closeConnectModal;
window.closeBuildModal = closeBuildModal;