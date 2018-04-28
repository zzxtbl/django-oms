<template>
  <transition :name="transitionName">
    <div class="back-to-ceiling" @click="backToTop" v-show="visible" :style="customStyle">
      <svg t="1524884210378" class="rocket" style="" viewBox="0 0 1024 1024" version="1.1"
           xmlns="http://www.w3.org/2000/svg" p-id="1198">
        <defs></defs>
        <path
          d="M662.72 462.784l136.448 169.408v173.248l-136.448-48.32zM342.72 457.344L206.272 626.816v173.248l136.448-48.384z"
          fill="#3A7EB9" p-id="1199"></path>
        <path
          d="M570.688 418.688l-142.848 1.152a266.496 266.496 0 0 1-20.288-0.576l3.712 448.64c0.256 28.928 94.272 130.048 94.272 130.048s93.888-102.656 93.632-131.584l-3.712-448.96a344.64 344.64 0 0 1-24.768 1.28z"
          fill="#ff9454" p-id="1200"></path>
        <path
          d="M531.456 599.296l-63.04 0.576c-3.008 0-5.952-0.064-8.96-0.384l2.176 257.792c0.128 16.64 41.728 74.816 41.728 74.816s41.344-58.944 41.28-75.52l-2.176-257.92c-3.648 0.384-7.296 0.64-11.008 0.64z"
          fill="#E9DF92" p-id="1201"></path>
        <path
          d="M554.304 93.568a324.352 324.352 0 0 0-110.592 1.728L342.72 240.768v584.512c13.824-0.96 27.968-1.536 42.368-1.536h245.248c11.84 0 23.36 0.384 34.816 1.024V253.312L554.304 93.568z"
          fill="#B5D5EB" p-id="1202"></path>
        <path
          d="M541.44 94.144L500.416 35.008l-45.696 59.136v29.504h89.024v-29.504zM459.456 288.64h88.96v88.896h-88.96zM459.456 467.456h88.96v88.96h-88.96zM459.456 634.176h88.96v88.896h-88.96zM364.928 788.736h277.76v44.352h-277.76z"
          fill="#ea94ff" p-id="1203"></path>
      </svg>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'BackToTop',
  props: {
    visibilityHeight: {
      type: Number,
      default: 400
    },
    backPosition: {
      type: Number,
      default: 0
    },
    customStyle: {
      type: Object,
      default: {
        right: '50px',
        bottom: '50px',
        width: '40px',
        height: '40px',
        'border-radius': '4px',
        'line-height': '45px'
      }
    },
    transitionName: {
      type: String,
      default: 'fade'
    }
  },
  data() {
    return {
      visible: false,
      interval: null
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll)
    if (this.interval) {
      clearInterval(this.interval)
    }
  },
  methods: {
    handleScroll() {
      this.visible = window.pageYOffset > this.visibilityHeight
    },
    backToTop() {
      const start = window.pageYOffset
      let i = 0
      this.interval = setInterval(() => {
        const next = Math.floor(this.easeInOutQuad(10 * i, start, -start, 500))
        if (next <= this.backPosition) {
          window.scrollTo(0, this.backPosition)
          clearInterval(this.interval)
        } else {
          window.scrollTo(0, next)
        }
        i++
      }, 16.7)
    },
    easeInOutQuad(t, b, c, d) {
      if ((t /= d / 2) < 1) return c / 2 * t * t + b
      return -c / 2 * (--t * (t - 2) - 1) + b
    }
  }
}
</script>

<style lang="scss">
  .back-to-ceiling {
    position: fixed;
    display: inline-block;
    text-align: center;
    cursor: pointer;
  }

  .rocket {
    fill: #9aaabf;
    background: none;
    animation: rocket-w 1.5s ease-in-out alternate infinite;
  }

  // 温柔的小火箭
  @-webkit-keyframes rocket-w {
    25% { transform: translateY(10px); }
    50% { transform: translateY(0); }
    75% { transform: translateY(10px); }
    100% { transform: translateY(0); }
  }

  // 变态的小火箭
  @-webkit-keyframes rocket-q {
    5% { transform: translateY(10px); }
    10% { transform: translateY(0); }
    15% { transform: translateY(10px); }
    20% { transform: translateY(0); }
    25% { transform: translateY(-10px); }
    30% { transform: translateY(0); }
    35% { transform: translateY(10px); }
    40% { transform: translateY(0); }
    45% { transform: translateY(10px); }
    50% { transform: translateY(0); }
    55% { transform: translateY(-10px); }
    60% { transform: translateY(0); }
    65% { transform: translateY(10px); }
    70% { transform: translateY(0); }
    75% { transform: translateY(10px); }
    80% { transform: translateY(0); }
    85% { transform: translateY(-10px); }
    90% { transform: translateY(0); }
    95% { transform: translateY(10px); }
    100% { transform: translateY(-50); }
  }
</style>
