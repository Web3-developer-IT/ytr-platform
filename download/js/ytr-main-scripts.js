/* =====================================================
   YTR - YOURS TO RENT - MAIN JAVASCRIPT
   South Africa's Premier Vehicle Marketplace
===================================================== */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    ytrInitPreloader();
    ytrInitNavigation();
    ytrInitCounters();
    ytrInitSwipers();
    ytrInitTabs();
    ytrInitRatingStars();
    ytrInitFavorites();
    ytrInitFAQ();
    ytrInitBackToTop();
    ytrInitAOS();
    ytrInitSAMap();
    ytrInitSearchForm();
    ytrInitEarningsCalculator();
});

/* =====================================================
   PRELOADER
===================================================== */
function ytrInitPreloader() {
    const preloader = document.getElementById('ytrPreloader');
    if (preloader) {
        window.addEventListener('load', function() {
            setTimeout(function() {
                preloader.classList.add('ytr-hidden');
            }, 500);
        });
    }
}

/* =====================================================
   NAVIGATION
===================================================== */
function ytrInitNavigation() {
    const nav = document.querySelector('.ytr-navigation-bar');
    const mobileToggle = document.getElementById('ytrMobileToggle');
    const mobileMenu = document.getElementById('ytrMobileMenu');
    
    // Scroll effect
    if (nav) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                nav.classList.add('ytr-nav-scrolled');
            } else {
                nav.classList.remove('ytr-nav-scrolled');
            }
        });
    }
    
    // Mobile menu toggle
    if (mobileToggle && mobileMenu) {
        mobileToggle.addEventListener('click', function() {
            this.classList.toggle('ytr-menu-active');
            mobileMenu.classList.toggle('ytr-mobile-menu-open');
        });
        
        // Close menu when clicking a link
        const mobileLinks = mobileMenu.querySelectorAll('a');
        mobileLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                mobileToggle.classList.remove('ytr-menu-active');
                mobileMenu.classList.remove('ytr-mobile-menu-open');
            });
        });
    }
}

/* =====================================================
   ANIMATED COUNTERS
===================================================== */
function ytrInitCounters() {
    const counters = document.querySelectorAll('.ytr-stat-number[data-count]');
    
    if (counters.length === 0) return;
    
    const observerOptions = {
        threshold: 0.5
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-count'));
                ytrAnimateCounter(counter, target);
                observer.unobserve(counter);
            }
        });
    }, observerOptions);
    
    counters.forEach(function(counter) {
        observer.observe(counter);
    });
}

function ytrAnimateCounter(element, target) {
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(function() {
        current += step;
        if (current >= target) {
            element.textContent = ytrFormatNumber(target);
            clearInterval(timer);
        } else {
            element.textContent = ytrFormatNumber(Math.floor(current));
        }
    }, 16);
}

function ytrFormatNumber(num) {
    if (num >= 1000) {
        return num.toLocaleString();
    }
    return num.toString();
}

/* =====================================================
   SWIPER CAROUSELS
===================================================== */
function ytrInitSwipers() {
    // Featured vehicles swiper
    const featuredSwiper = document.querySelector('.ytr-featured-swiper');
    if (featuredSwiper) {
        const Swiper = window.Swiper; // Declare Swiper variable
        new Swiper('.ytr-featured-swiper', {
            slidesPerView: 1,
            spaceBetween: 20,
            loop: true,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.ytr-swiper-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.ytr-swiper-button-next',
                prevEl: '.ytr-swiper-button-prev',
            },
            breakpoints: {
                576: {
                    slidesPerView: 2,
                },
                992: {
                    slidesPerView: 3,
                },
                1200: {
                    slidesPerView: 4,
                },
            },
        });
    }
    
    // Testimonials swiper
    const testimonialsSwiper = document.querySelector('.ytr-testimonials-swiper');
    if (testimonialsSwiper) {
        const Swiper = window.Swiper; // Declare Swiper variable
        new Swiper('.ytr-testimonials-swiper', {
            slidesPerView: 1,
            spaceBetween: 20,
            loop: true,
            autoplay: {
                delay: 6000,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.ytr-testimonials-pagination',
                clickable: true,
            },
            breakpoints: {
                768: {
                    slidesPerView: 2,
                },
                1200: {
                    slidesPerView: 3,
                },
            },
        });
    }
}

/* =====================================================
   TABS
===================================================== */
function ytrInitTabs() {
    // How It Works tabs
    const howTabs = document.querySelectorAll('.ytr-how-tab');
    howTabs.forEach(function(tab) {
        tab.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Remove active from all tabs
            howTabs.forEach(function(t) {
                t.classList.remove('ytr-how-tab-active');
            });
            
            // Add active to clicked tab
            this.classList.add('ytr-how-tab-active');
            
            // Hide all content
            document.querySelectorAll('.ytr-how-content').forEach(function(content) {
                content.classList.remove('ytr-how-content-active');
            });
            
            // Show selected content
            const selectedContent = document.getElementById('ytr-how-' + tabId);
            if (selectedContent) {
                selectedContent.classList.add('ytr-how-content-active');
            }
        });
    });
    
    // Feedback tabs
    const feedbackTabs = document.querySelectorAll('.ytr-feedback-tab');
    feedbackTabs.forEach(function(tab) {
        tab.addEventListener('click', function() {
            feedbackTabs.forEach(function(t) {
                t.classList.remove('ytr-feedback-tab-active');
            });
            this.classList.add('ytr-feedback-tab-active');
        });
    });
}

/* =====================================================
   RATING STARS
===================================================== */
function ytrInitRatingStars() {
    const ratingContainers = document.querySelectorAll('.ytr-rating-stars');
    
    ratingContainers.forEach(function(container) {
        const stars = container.querySelectorAll('i');
        let selectedRating = 0;
        
        stars.forEach(function(star, index) {
            star.addEventListener('mouseenter', function() {
                ytrHighlightStars(stars, index + 1);
            });
            
            star.addEventListener('mouseleave', function() {
                ytrHighlightStars(stars, selectedRating);
            });
            
            star.addEventListener('click', function() {
                selectedRating = index + 1;
                ytrHighlightStars(stars, selectedRating);
            });
        });
    });
}

function ytrHighlightStars(stars, count) {
    stars.forEach(function(star, index) {
        if (index < count) {
            star.classList.remove('far');
            star.classList.add('fas', 'ytr-star-active');
        } else {
            star.classList.remove('fas', 'ytr-star-active');
            star.classList.add('far');
        }
    });
}

/* =====================================================
   FAVORITES
===================================================== */
function ytrInitFavorites() {
    const favoriteButtons = document.querySelectorAll('.ytr-vehicle-favorite');
    
    favoriteButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            this.classList.toggle('ytr-favorited');
            
            const icon = this.querySelector('i');
            if (this.classList.contains('ytr-favorited')) {
                icon.classList.remove('far');
                icon.classList.add('fas');
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
            }
        });
    });
}

/* =====================================================
   FAQ ACCORDION
===================================================== */
function ytrInitFAQ() {
    const faqItems = document.querySelectorAll('.ytr-faq-item');
    
    faqItems.forEach(function(item) {
        const question = item.querySelector('.ytr-faq-question');
        
        if (question) {
            question.addEventListener('click', function() {
                // Close other items
                faqItems.forEach(function(otherItem) {
                    if (otherItem !== item) {
                        otherItem.classList.remove('ytr-faq-open');
                    }
                });
                
                // Toggle current item
                item.classList.toggle('ytr-faq-open');
            });
        }
    });
}

/* =====================================================
   BACK TO TOP
===================================================== */
function ytrInitBackToTop() {
    const backToTop = document.getElementById('ytrBackToTop');
    
    if (backToTop) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 500) {
                backToTop.classList.add('ytr-visible');
            } else {
                backToTop.classList.remove('ytr-visible');
            }
        });
        
        backToTop.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

/* =====================================================
   AOS (ANIMATE ON SCROLL)
===================================================== */
function ytrInitAOS() {
    const AOS = window.AOS; // Declare AOS variable
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-out',
            once: true,
            offset: 50
        });
    }
}

/* =====================================================
   SOUTH AFRICA MAP (VISUAL ONLY)
===================================================== */
function ytrInitSAMap() {
    const mapWrapper = document.querySelector('.ytr-sa-map-wrapper');
    if (!mapWrapper) return;
    
    const tooltip = document.querySelector('.ytr-map-tooltip');
    const provinces = document.querySelectorAll('.ytr-province-path');
    
    provinces.forEach(function(province) {
        province.addEventListener('mouseenter', function(e) {
            const name = this.getAttribute('data-name');
            const region = this.getAttribute('data-region');
            
            if (tooltip) {
                const titleEl = tooltip.querySelector('.ytr-map-tooltip-title');
                const regionEl = tooltip.querySelector('.ytr-map-tooltip-region');
                
                if (titleEl) titleEl.textContent = name;
                if (regionEl) regionEl.textContent = region;
                
                tooltip.classList.add('ytr-tooltip-visible');
            }
        });
        
        province.addEventListener('mousemove', function(e) {
            if (tooltip) {
                const rect = mapWrapper.getBoundingClientRect();
                const x = e.clientX - rect.left + 15;
                const y = e.clientY - rect.top - 10;
                
                tooltip.style.left = x + 'px';
                tooltip.style.top = y + 'px';
            }
        });
        
        province.addEventListener('mouseleave', function() {
            if (tooltip) {
                tooltip.classList.remove('ytr-tooltip-visible');
            }
        });
    });
}

/* =====================================================
   SEARCH FORM
===================================================== */
function ytrInitSearchForm() {
    const searchForm = document.querySelector('.ytr-search-form');
    
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Visual feedback only - redirect to browse page
            window.location.href = 'browse.html';
        });
    }
    
    // Set minimum dates for date inputs
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    
    dateInputs.forEach(function(input) {
        input.setAttribute('min', today);
    });
}

/* =====================================================
   EARNINGS CALCULATOR
===================================================== */
function ytrInitEarningsCalculator() {
    const calcWrapper = document.querySelector('.ytr-earnings-calculator');
    if (!calcWrapper) return;
    
    const rateInput = calcWrapper.querySelector('input[type="number"]');
    const daysSelect = calcWrapper.querySelector('select');
    const resultAmount = calcWrapper.querySelector('.ytr-calc-result-amount');
    
    function calculateEarnings() {
        if (!rateInput || !daysSelect || !resultAmount) return;
        
        const rate = parseFloat(rateInput.value) || 0;
        const days = parseInt(daysSelect.value) || 0;
        const earnings = rate * days;
        
        resultAmount.textContent = 'R' + earnings.toLocaleString();
    }
    
    if (rateInput) {
        rateInput.addEventListener('input', calculateEarnings);
    }
    
    if (daysSelect) {
        daysSelect.addEventListener('change', calculateEarnings);
    }
    
    // Initial calculation
    calculateEarnings();
}

/* =====================================================
   VEHICLE GALLERY
===================================================== */
function ytrInitGallery() {
    const mainImage = document.querySelector('.ytr-gallery-main img');
    const thumbnails = document.querySelectorAll('.ytr-gallery-thumb');
    
    thumbnails.forEach(function(thumb) {
        thumb.addEventListener('click', function() {
            const imgSrc = this.querySelector('img').src;
            
            // Update main image
            if (mainImage) {
                mainImage.src = imgSrc;
            }
            
            // Update active state
            thumbnails.forEach(function(t) {
                t.classList.remove('ytr-thumb-active');
            });
            this.classList.add('ytr-thumb-active');
        });
    });
}

/* =====================================================
   FILTER PILLS (Browse Page)
===================================================== */
function ytrInitFilterPills() {
    const filterPills = document.querySelectorAll('.ytr-filter-pill');
    
    filterPills.forEach(function(pill) {
        pill.addEventListener('click', function() {
            filterPills.forEach(function(p) {
                p.classList.remove('ytr-filter-pill-active');
            });
            this.classList.add('ytr-filter-pill-active');
            
            // Visual feedback only - no actual filtering
            const vehicleGrid = document.querySelector('.ytr-browse-grid');
            if (vehicleGrid) {
                vehicleGrid.style.opacity = '0.5';
                setTimeout(function() {
                    vehicleGrid.style.opacity = '1';
                }, 300);
            }
        });
    });
}

/* =====================================================
   VIEW TOGGLE (Grid/List)
===================================================== */
function ytrInitViewToggle() {
    const viewButtons = document.querySelectorAll('.ytr-view-btn');
    const browseGrid = document.querySelector('.ytr-browse-grid');
    
    viewButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            viewButtons.forEach(function(b) {
                b.classList.remove('ytr-view-btn-active');
            });
            this.classList.add('ytr-view-btn-active');
            
            // Visual feedback only
            if (browseGrid) {
                browseGrid.style.opacity = '0.5';
                setTimeout(function() {
                    browseGrid.style.opacity = '1';
                }, 200);
            }
        });
    });
}

/* =====================================================
   FORM VALIDATION (Visual Only)
===================================================== */
function ytrInitFormValidation() {
    const forms = document.querySelectorAll('.ytr-contact-form, .ytr-feedback-form, .ytr-auth-form');
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Visual success feedback
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-check"></i> Submitted!';
                submitBtn.style.background = '#10b981';
                
                setTimeout(function() {
                    submitBtn.innerHTML = originalText;
                    submitBtn.style.background = '';
                    form.reset();
                }, 2000);
            }
        });
    });
}

/* =====================================================
   NEWSLETTER FORM
===================================================== */
function ytrInitNewsletter() {
    const newsletterForm = document.querySelector('.ytr-newsletter-form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('button');
            const input = this.querySelector('input');
            
            if (submitBtn && input && input.value) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-check"></i>';
                
                setTimeout(function() {
                    submitBtn.innerHTML = originalText;
                    input.value = '';
                }, 2000);
            }
        });
    }
}

/* =====================================================
   LIVE TIME DISPLAY
===================================================== */
function ytrInitLiveTime() {
    const timeElement = document.querySelector('.ytr-live-time');
    
    if (timeElement) {
        function updateTime() {
            const now = new Date();
            const options = {
                timeZone: 'Africa/Johannesburg',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            };
            timeElement.textContent = now.toLocaleTimeString('en-ZA', options) + ' SAST';
        }
        
        updateTime();
        setInterval(updateTime, 1000);
    }
}

/* =====================================================
   SMOOTH SCROLL FOR ANCHOR LINKS
===================================================== */
document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            e.preventDefault();
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

/* =====================================================
   SCROLL INDICATOR
===================================================== */
const scrollIndicator = document.querySelector('.ytr-hero-scroll-indicator');
if (scrollIndicator) {
    scrollIndicator.addEventListener('click', function() {
        const searchSection = document.getElementById('search');
        if (searchSection) {
            searchSection.scrollIntoView({
                behavior: 'smooth'
            });
        } else {
            window.scrollBy({
                top: window.innerHeight * 0.8,
                behavior: 'smooth'
            });
        }
    });
}

/* =====================================================
   INITIALIZE ADDITIONAL FUNCTIONS ON PAGE LOAD
===================================================== */
window.addEventListener('load', function() {
    ytrInitGallery();
    ytrInitFilterPills();
    ytrInitViewToggle();
    ytrInitFormValidation();
    ytrInitNewsletter();
    ytrInitLiveTime();
});
