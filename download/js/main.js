/* ============================================
   YOURS TO RENT - MAIN JAVASCRIPT
   ============================================ */

// Import necessary libraries
import bootstrap from "bootstrap"
import AOS from "aos"
import Swiper from "swiper/bundle"

document.addEventListener("DOMContentLoaded", () => {
  // Initialize all components
  initPreloader()
  initNavbar()
  initAOS()
  initSwipers()
  initCounters()
  initPriceRange()
  initTabs()
  initFavorites()
  initBackToTop()
  initFormValidation()
  initDropdowns()
  initModals()
  initAccordions()
  initSearchForm()
  initLazyLoading()
})

/* ============================================
   PRELOADER
   ============================================ */
function initPreloader() {
  const preloader = document.getElementById("preloader")
  if (preloader) {
    window.addEventListener("load", () => {
      setTimeout(() => {
        preloader.classList.add("hidden")
      }, 500)
    })
  }
}

/* ============================================
   NAVBAR
   ============================================ */
function initNavbar() {
  const navbar = document.getElementById("mainNav")

  if (navbar) {
    // Scroll effect
    window.addEventListener("scroll", () => {
      if (window.scrollY > 100) {
        navbar.classList.add("scrolled")
      } else {
        navbar.classList.remove("scrolled")
      }
    })

    // Close mobile menu on link click
    const navLinks = document.querySelectorAll(".navbar-nav .nav-link")
    const navbarCollapse = document.getElementById("navbarNav")

    navLinks.forEach((link) => {
      link.addEventListener("click", () => {
        if (navbarCollapse.classList.contains("show")) {
          new bootstrap.Collapse(navbarCollapse).hide()
        }
      })
    })
  }
}

/* ============================================
   AOS ANIMATIONS
   ============================================ */
function initAOS() {
  if (typeof AOS !== "undefined") {
    AOS.init({
      duration: 800,
      easing: "ease-out-cubic",
      once: true,
      offset: 50,
      delay: 0,
    })
  }
}

/* ============================================
   SWIPER SLIDERS
   ============================================ */
function initSwipers() {
  // Featured Vehicles Swiper
  const featuredSwiper = document.querySelector(".featured-swiper")
  if (featuredSwiper) {
    new Swiper(".featured-swiper", {
      slidesPerView: 1,
      spaceBetween: 24,
      loop: true,
      autoplay: {
        delay: 5000,
        disableOnInteraction: false,
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      navigation: {
        nextEl: ".swiper-btn-next",
        prevEl: ".swiper-btn-prev",
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
    })
  }

  // Testimonials Swiper
  const testimonialsSwiper = document.querySelector(".testimonials-swiper")
  if (testimonialsSwiper) {
    new Swiper(".testimonials-swiper", {
      slidesPerView: 1,
      spaceBetween: 24,
      loop: true,
      autoplay: {
        delay: 6000,
        disableOnInteraction: false,
      },
      pagination: {
        el: ".swiper-pagination",
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
    })
  }

  // Vehicle Gallery Swiper (for detail pages)
  const gallerySwiper = document.querySelector(".gallery-swiper")
  if (gallerySwiper) {
    const thumbsSwiper = new Swiper(".gallery-thumbs", {
      spaceBetween: 10,
      slidesPerView: 5,
      freeMode: true,
      watchSlidesProgress: true,
    })

    new Swiper(".gallery-swiper", {
      spaceBetween: 10,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      thumbs: {
        swiper: thumbsSwiper,
      },
    })
  }
}

/* ============================================
   ANIMATED COUNTERS
   ============================================ */
function initCounters() {
  const counters = document.querySelectorAll("[data-count]")

  if (counters.length > 0) {
    const observerOptions = {
      threshold: 0.5,
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCounter(entry.target)
          observer.unobserve(entry.target)
        }
      })
    }, observerOptions)

    counters.forEach((counter) => {
      observer.observe(counter)
    })
  }
}

function animateCounter(element) {
  const target = Number.parseInt(element.getAttribute("data-count"))
  const duration = 2000
  const step = target / (duration / 16)
  let current = 0

  const timer = setInterval(() => {
    current += step
    if (current >= target) {
      element.textContent = formatNumber(target)
      clearInterval(timer)
    } else {
      element.textContent = formatNumber(Math.floor(current))
    }
  }, 16)
}

function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

/* ============================================
   PRICE RANGE SLIDER
   ============================================ */
function initPriceRange() {
  const priceRange = document.getElementById("priceRange")
  const currentPrice = document.querySelector(".current-price")

  if (priceRange && currentPrice) {
    priceRange.addEventListener("input", function () {
      const value = this.value
      currentPrice.textContent = "R" + formatNumber(value)

      // Update gradient position
      const percent = ((value - this.min) / (this.max - this.min)) * 100
      this.style.background = `linear-gradient(to right, #FFD700 0%, #FF8C00 ${percent}%, #333 ${percent}%)`
    })

    // Initialize
    priceRange.dispatchEvent(new Event("input"))
  }
}

/* ============================================
   TAB NAVIGATION
   ============================================ */
function initTabs() {
  // How It Works Tabs
  const howTabs = document.querySelectorAll(".how-tab")
  const howContents = document.querySelectorAll(".how-content")

  howTabs.forEach((tab) => {
    tab.addEventListener("click", function () {
      const target = this.getAttribute("data-tab")

      // Remove active from all tabs
      howTabs.forEach((t) => t.classList.remove("active"))
      howContents.forEach((c) => c.classList.remove("active"))

      // Add active to clicked tab
      this.classList.add("active")
      document.getElementById(target + "-content").classList.add("active")
    })
  })

  // Generic Tab Navigation
  const tabBtns = document.querySelectorAll(".tab-btn")

  tabBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const tabGroup = this.closest(".tabs-container") || this.closest(".tabs-pill")?.parentElement
      if (!tabGroup) return

      const tabs = tabGroup.querySelectorAll(".tab-btn")
      const contents = tabGroup.querySelectorAll(".tab-content")
      const target = this.getAttribute("data-tab")

      tabs.forEach((t) => t.classList.remove("active"))
      contents.forEach((c) => c.classList.remove("active"))

      this.classList.add("active")
      const targetContent = document.getElementById(target)
      if (targetContent) {
        targetContent.classList.add("active")
      }
    })
  })
}

/* ============================================
   FAVORITES TOGGLE
   ============================================ */
function initFavorites() {
  const favoriteButtons = document.querySelectorAll(".favorite-btn")

  favoriteButtons.forEach((btn) => {
    btn.addEventListener("click", function (e) {
      e.preventDefault()
      e.stopPropagation()

      this.classList.toggle("active")
      const icon = this.querySelector("i")

      if (this.classList.contains("active")) {
        icon.classList.remove("far")
        icon.classList.add("fas")
        showToast("Added to favorites!", "success")
      } else {
        icon.classList.remove("fas")
        icon.classList.add("far")
        showToast("Removed from favorites", "info")
      }
    })
  })
}

/* ============================================
   BACK TO TOP BUTTON
   ============================================ */
function initBackToTop() {
  const backToTop = document.getElementById("backToTop")

  if (backToTop) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 500) {
        backToTop.classList.add("visible")
      } else {
        backToTop.classList.remove("visible")
      }
    })

    backToTop.addEventListener("click", () => {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      })
    })
  }
}

/* ============================================
   FORM VALIDATION
   ============================================ */
function initFormValidation() {
  const forms = document.querySelectorAll("form[data-validate]")

  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      let isValid = true
      const requiredFields = this.querySelectorAll("[required]")

      requiredFields.forEach((field) => {
        if (!field.value.trim()) {
          isValid = false
          showFieldError(field, "This field is required")
        } else {
          clearFieldError(field)

          // Email validation
          if (field.type === "email" && !isValidEmail(field.value)) {
            isValid = false
            showFieldError(field, "Please enter a valid email")
          }

          // Phone validation
          if (field.type === "tel" && !isValidPhone(field.value)) {
            isValid = false
            showFieldError(field, "Please enter a valid phone number")
          }
        }
      })

      if (!isValid) {
        e.preventDefault()
      }
    })
  })
}

function showFieldError(field, message) {
  field.classList.add("is-invalid")
  let errorDiv = field.parentElement.querySelector(".invalid-feedback")

  if (!errorDiv) {
    errorDiv = document.createElement("div")
    errorDiv.className = "invalid-feedback"
    field.parentElement.appendChild(errorDiv)
  }

  errorDiv.textContent = message
}

function clearFieldError(field) {
  field.classList.remove("is-invalid")
  const errorDiv = field.parentElement.querySelector(".invalid-feedback")
  if (errorDiv) {
    errorDiv.remove()
  }
}

function isValidEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

function isValidPhone(phone) {
  const re = /^[\d\s\-+$$$$]{10,}$/
  return re.test(phone)
}

/* ============================================
   DROPDOWN HANDLING
   ============================================ */
function initDropdowns() {
  const dropdowns = document.querySelectorAll(".dropdown-custom")

  dropdowns.forEach((dropdown) => {
    const trigger = dropdown.querySelector(".dropdown-trigger")

    if (trigger) {
      trigger.addEventListener("click", (e) => {
        e.stopPropagation()

        // Close other dropdowns
        dropdowns.forEach((d) => {
          if (d !== dropdown) {
            d.classList.remove("active")
          }
        })

        dropdown.classList.toggle("active")
      })
    }
  })

  // Close dropdowns when clicking outside
  document.addEventListener("click", () => {
    dropdowns.forEach((d) => d.classList.remove("active"))
  })
}

/* ============================================
   MODAL HANDLING
   ============================================ */
function initModals() {
  const modalTriggers = document.querySelectorAll("[data-modal]")
  const modalCloses = document.querySelectorAll(".modal-close, .modal-overlay")

  modalTriggers.forEach((trigger) => {
    trigger.addEventListener("click", function (e) {
      e.preventDefault()
      const modalId = this.getAttribute("data-modal")
      const modal = document.getElementById(modalId)

      if (modal) {
        modal.classList.add("active")
        document.body.style.overflow = "hidden"
      }
    })
  })

  modalCloses.forEach((close) => {
    close.addEventListener("click", function (e) {
      if (e.target === this) {
        const modal = this.closest(".modal-overlay")
        if (modal) {
          modal.classList.remove("active")
          document.body.style.overflow = ""
        }
      }
    })
  })

  // Close on Escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      const activeModal = document.querySelector(".modal-overlay.active")
      if (activeModal) {
        activeModal.classList.remove("active")
        document.body.style.overflow = ""
      }
    }
  })
}

/* ============================================
   ACCORDION HANDLING
   ============================================ */
function initAccordions() {
  const accordionHeaders = document.querySelectorAll(".accordion-header-custom")

  accordionHeaders.forEach((header) => {
    header.addEventListener("click", function () {
      const item = this.closest(".accordion-item-custom")
      const isActive = item.classList.contains("active")

      // Close all accordion items in the same group
      const parent = item.parentElement
      parent.querySelectorAll(".accordion-item-custom").forEach((i) => {
        i.classList.remove("active")
      })

      // Toggle current item
      if (!isActive) {
        item.classList.add("active")
      }
    })
  })
}

/* ============================================
   SEARCH FORM HANDLING
   ============================================ */
function initSearchForm() {
  const searchForm = document.querySelector(".search-form")

  if (searchForm) {
    // Set minimum date to today
    const dateInputs = searchForm.querySelectorAll('input[type="date"]')
    const today = new Date().toISOString().split("T")[0]

    dateInputs.forEach((input) => {
      input.setAttribute("min", today)
    })

    // Validate return date is after pickup date
    const pickupDate = searchForm.querySelector('[name="pickup_date"]')
    const returnDate = searchForm.querySelector('[name="return_date"]')

    if (pickupDate && returnDate) {
      pickupDate.addEventListener("change", function () {
        returnDate.setAttribute("min", this.value)
        if (returnDate.value && returnDate.value < this.value) {
          returnDate.value = this.value
        }
      })
    }
  }
}

/* ============================================
   TOAST NOTIFICATIONS
   ============================================ */
function showToast(message, type = "info") {
  // Remove existing toasts
  const existingToast = document.querySelector(".toast-notification")
  if (existingToast) {
    existingToast.remove()
  }

  // Create toast element
  const toast = document.createElement("div")
  toast.className = `toast-notification toast-${type}`
  toast.innerHTML = `
        <i class="fas fa-${getToastIcon(type)}"></i>
        <span>${message}</span>
    `

  // Add styles
  Object.assign(toast.style, {
    position: "fixed",
    bottom: "20px",
    right: "20px",
    padding: "16px 24px",
    background: "var(--bg-dark-3)",
    border: "1px solid var(--border-dark)",
    borderRadius: "var(--radius-md)",
    color: "var(--text-white)",
    display: "flex",
    alignItems: "center",
    gap: "12px",
    boxShadow: "var(--shadow-lg)",
    zIndex: "9999",
    animation: "slideInRight 0.3s ease",
  })

  document.body.appendChild(toast)

  // Remove after 3 seconds
  setTimeout(() => {
    toast.style.animation = "slideOutRight 0.3s ease"
    setTimeout(() => {
      toast.remove()
    }, 300)
  }, 3000)
}

function getToastIcon(type) {
  const icons = {
    success: "check-circle",
    error: "exclamation-circle",
    warning: "exclamation-triangle",
    info: "info-circle",
  }
  return icons[type] || icons.info
}

// Add toast animations
const toastStyles = document.createElement("style")
toastStyles.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .toast-success i { color: #10B981; }
    .toast-error i { color: #EF4444; }
    .toast-warning i { color: #F59E0B; }
    .toast-info i { color: #3B82F6; }
`
document.head.appendChild(toastStyles)

/* ============================================
   LAZY LOADING IMAGES
   ============================================ */
function initLazyLoading() {
  const lazyImages = document.querySelectorAll("img[data-src]")

  if ("IntersectionObserver" in window) {
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target
          img.src = img.dataset.src
          img.classList.add("loaded")
          imageObserver.unobserve(img)
        }
      })
    })

    lazyImages.forEach((img) => {
      imageObserver.observe(img)
    })
  } else {
    // Fallback for older browsers
    lazyImages.forEach((img) => {
      img.src = img.dataset.src
    })
  }
}

/* ============================================
   SMOOTH SCROLL FOR ANCHOR LINKS
   ============================================ */
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    const targetId = this.getAttribute("href")
    if (targetId === "#") return

    const target = document.querySelector(targetId)
    if (target) {
      e.preventDefault()
      const navHeight = document.getElementById("mainNav")?.offsetHeight || 0
      const targetPosition = target.offsetTop - navHeight - 20

      window.scrollTo({
        top: targetPosition,
        behavior: "smooth",
      })
    }
  })
})

/* ============================================
   UTILITIES
   ============================================ */

// Debounce function
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// Throttle function
function throttle(func, limit) {
  let inThrottle
  return function (...args) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}

// Format currency
function formatCurrency(amount) {
  return "R" + amount.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, "$&,")
}

// Get URL parameter
function getUrlParam(param) {
  const urlParams = new URLSearchParams(window.location.search)
  return urlParams.get(param)
}

// Set URL parameter
function setUrlParam(param, value) {
  const url = new URL(window.location)
  url.searchParams.set(param, value)
  window.history.pushState({}, "", url)
}

// Copy to clipboard
function copyToClipboard(text) {
  navigator.clipboard
    .writeText(text)
    .then(() => {
      showToast("Copied to clipboard!", "success")
    })
    .catch(() => {
      showToast("Failed to copy", "error")
    })
}

// Console message
console.log("%c🚗 Yours To Rent", "font-size: 24px; font-weight: bold; color: #FFD700;")
console.log("%cYour Fleet. Your Services. Your Terms.", "font-size: 14px; color: #888;")
