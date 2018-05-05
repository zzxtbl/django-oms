<template>
  <div class="components-container" style='height:100vh'>
        <el-card>
        </el-card>
  </div>
</template>

<script>
import { LIMIT } from '@/config'

export default {
  components: {},

  data() {
    return {
      status: true,
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      limit: LIMIT,
      offset: '',
      pagesize: [10, 25, 50, 100]
    }
  },
  created() {
  },
  methods: {
    searchClick() {
      this.fetchData()
    },
    handleSizeChange(val) {
      this.limit = val
      this.fetchData()
    },
    handleCurrentChange(val) {
      this.offset = (val - 1) * LIMIT
      this.fetchData()
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .title {
    color: #94acff;
    font-size: 20px;
  }

  .panel-group {
    margin-top: 18px;
    .card-panel-col {
      margin-bottom: 32px;
    }
    .card-panel {
      cursor: pointer;
      font-size: 12px;
      position: relative;
      overflow: hidden;
      color: #666;
      background: #fff;
      box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
      border-color: rgba(0, 0, 0, .05);
      &:hover {
        .card-panel-icon-wrapper {
          color: #fff;
        }
        .icon-people {
          background: #40c9c6;
        }
        .icon-message {
          background: #f4516c;
        }
        .icon-money {
          background: #4b4b4b;
        }
        .icon-shoppingCard {
          background: #f4516c
        }
      }
      .icon-people {
        color: #40c9c6;
      }
      .icon-message {
        color: #f4516c;
      }
      .icon-money {
        color: #4b4b4b;
      }
      .icon-shoppingCard {
        color: #f4516c
      }
      .card-panel-icon-wrapper {
        float: left;
        margin: 14px 0 0 14px;
        padding: 14px;
        transition: all 0.5s ease-out;
        border-radius: 6px;
        border: solid 1px;
      }
      .wenzi {
        font-size: 24px;
      }
      .card-panel-description {
        float: right;
        font-weight: bold;
        margin: 26px;
        .card-panel-text {
          line-height: 18px;
          color: rgba(0, 0, 0, 0.45);
          font-size: 16px;
          margin-bottom: 12px;
        }
        .card-panel-num {
          font-size: 20px;
        }
      }
    }
  }

  .head-lavel {
    padding-bottom: 50px;
  }

  .table-button {
    padding: 10px 0;
    float: left;
  }

  .table-search {
    float: right;
    padding: 10px 0;
  }

  .table-pagination {
    padding: 10px 0;
    float: right;
  }
</style>
