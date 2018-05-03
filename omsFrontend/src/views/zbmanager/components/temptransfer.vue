<template>
  <div>
    <div>
      <el-transfer
        v-model="value"
        filterable
        :titles="['未选择', '已选择']"
        :button-texts="['向左走', '向右走']"
        @change="handleChange"
        :data="alldata">
      </el-transfer>
    </div>
  </div>
</template>

<script>
import { getzkTemplate } from 'api/zabbix'

export default {
  props: ['selectdata'],
  data() {
    return {
      alldata: [],
      value: this.selectdata,
      changedata: false
    }
  },

  created() {
    this.getData()
  },

  methods: {
    getData() {
      this.alldata = []
      this.value = this.selectdata
      getzkTemplate().then(response => {
        this.alldata = []
        const results = response.data
        for (var i = 0, len = results.length; i < len; i++) {
          this.alldata.push({
            label: results[i].host,
            key: results[i].templateid
          })
        }
      })
    },
    handleChange(value, direction, movedKeys) {
      this.$emit('getDatas', value)
    }
  }
//  watch: {
//    // 监控rowdata值的变化，有变化立即刷新数据
//    selectdata() {
//      this.getData()
//    }
//  }
}
</script>

<style>
  .transfer-footer {
    margin-left: 20px;
    padding: 6px 5px;
  }
</style>
