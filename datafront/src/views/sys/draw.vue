<!-- <template>
  <div class="container">
    <div class="left">
      <div class="button-group">
        <el-button type="primary" style="margin:10px 22px;" @click="getChecked">Render graph</el-button>
        <el-button type="info" style="margin:10px 0;" @click="cancelSelection">Cancel selection</el-button>
      </div>
      <div class="tree-wrapper">
        <el-tree :props="props" ref="tree" :load="loadNode" lazy :show-checkbox="false" :check-on-click-node="true"
          @check="handleCheck" :key="componentKey">
          <template #default="{ node, data }">
            <div class="custom-tree-node" @mouseenter="mouseenter(node)" @mouseleave="mouseleave(node)">
              <span>
                <el-checkbox v-if="data.isleaf" :checked="node.checked" @change="handleCheck(node)">
                </el-checkbox>
                {{ node.label }}
              </span>
              <el-button v-show="node.showExtra" type="danger" :icon="Delete" class="delete-button"
                @click="remove(node, data)">
              </el-button>
            </div>
          </template>
        </el-tree>
      </div>
    </div>
    <div class="right">
      <GraphViewer :graph-info="graph_info" />
    </div>
  </div>
</template> -->
<template>
  <div class="container">
    <div class="left">
      <div class="button-group">
        <el-button type="primary" style="margin:10px 22px;" @click="getChecked">Render graph</el-button>
        <el-button type="info" style="margin:10px 22px;" @click="cancelSelection">Cancel selection</el-button>
      </div>
    <div class="tree-wrapper">
      <el-tree
        :props="props"
        ref="tree"
        :load="loadNode"
        lazy
        :show-checkbox="false"
        :check-strictly="true"
        :check-on-click-node="true"
        @check="handleCheck"
        :key="componentKey"
      >
      <template #default="{ node, data }">
        <div class="custom-tree-node" @mouseenter="mouseenter(node)" @mouseleave="mouseleave(node)">
          <div class="node-content">
            <el-checkbox v-show="node.isLeaf" v-model="node.checked" class="node-checkbox"></el-checkbox>
            <span>{{ node.label }}</span>
          </div>
          <el-button v-show="node.showExtra" type="danger" :icon="Delete" class="delete-button" @click="remove(node, data)">
          </el-button>
        </div>
      </template>
      </el-tree>
    </div>
  </div>
  <div class="right">
    <GraphViewer :graph-info="graph_info" />
  </div>
  </div>
</template>

<script setup>
import { Check, Delete, Edit, Message, Search, Star, } from '@element-plus/icons-vue'
import { NODE_RADIUS, json2vNG, vNG2Json } from '@/util/graph.js';
import GraphViewer from '@/components/GraphViewer.vue';
import { ref, onMounted, nextTick } from 'vue'
// import * as echarts from 'echarts'; 
import { getfirData, getsecData, getthrData, getfouData, getfivData, darwgeo, delnode } from '@/util/base.js'
import { ElMessage, ElMessageBox } from 'element-plus'

const props = { 
  label: 'title', 
  isLeaf: 'isleaf', 
}
let tree = ref('')
let componentKey = ref(0)
const graph_info = ref();

const loadfirstnode = async function (resolve) {
  const res = await getfirData();
  return resolve(res);
}
const loadsecnode = async function (node, resolve) {
  let params = {
    batchno: node.data.name,
  };
  const res = await getsecData(params);
  return resolve(res);
}

const loadthrnode = async function (node, resolve) {
  let params = {
    batchno: node.parent.data.name,
    season: node.data.name
  };
  const res = await getthrData(params);
  return resolve(res);
}
const loadfounode = async function (node, resolve) {
  let params = {
    batchno: node.parent.parent.data.name,
    season: node.parent.data.name,
    episode: node.data.name
  };
  const res = await getfouData(params);
  return resolve(res);
}

const loadfivnode = async function (node, resolve) {
  let params = {
    batchno: node.parent.parent.parent.data.name,
    season: node.parent.parent.data.name,
    episode: node.parent.data.name,
    scene: node.data.name,
  };
  const res = await getfivData(params);
  let newres = []
  res.forEach(function (item) {
    if (item.isleaf == 1) {
      newres.push({ name: item.name, isleaf: true, title: item.title, relate: item.relate })
    }
  })
  return resolve(newres);
}
const loadNode = (node, resolve) => {
  console.log('调用了', node)
  if (node.level === 0) {
    //   return resolve([{ name: 'region' }])
    loadfirstnode(resolve)
  }
  else if (node.level === 1) {
    loadsecnode(node, resolve);
  }
  else if (node.level === 2) {
    loadthrnode(node, resolve);

  }
  else if (node.level === 3) {
    loadfounode(node, resolve);
  }
  else if (node.level === 4) {
    loadfivnode(node, resolve);
  }
}
const getChecked = async function () {
  const checkedNodes = tree.value.getCheckedNodes();
  console.log('ciao', checkedNodes); // 打印选中的节点数据
  if (!checkedNodes.length) {
    ElMessage({
      message: 'please select node',
      type: 'error',
    })
    return
  }

  const flag = checkedNodes.some(item => {
    return item.isleaf
  })
  if (!flag) {
    ElMessage({
      message: 'no leaf node selected',
      type: 'error',
    })
    return
  }
  const leafselect = checkedNodes.filter(item => {
    if (item.isleaf) {
      return item
    }
  })
  console.log(leafselect)
  if (leafselect.length > 2) {
    ElMessage({
      message: 'at most two leaf nodes can be selected',
      type: 'error',
    })
    return
  }

  let res = await darwgeo(leafselect)
  console.log("data:", res.data)
  graph_info.value = json2vNG(res.data);
  console.log("graph_info:", graph_info)
}

const cancelSelection = () => {
  const checkedNodes = tree.value.getCheckedNodes();
  checkedNodes.forEach(node => {
    tree.value.setChecked(node, false, false);
    node.checked = false;
  });
  // componentKey.value += 1; // Force update the component
};

const remove = async function (node, data) {
  // console.log(node);
  console.log(data)
  ElMessageBox.confirm(
    'Are you sure you want to delete this record',
    'Warning',
    {
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
  ).then(async () => {
    await delnode(data).then(res => {
      if (res.code === 200) {
        ElMessage({
          message: res.msg,
          type: 'success',
        })
        componentKey.value += 1
      }
    }).catch(error => {
      ElMessage({
        message: 'Delete failed',
        type: 'error',
      })

    })
  }

  ).catch(() => {
    ElMessage({
      type: 'info',
      message: 'Delete canceled',
    })
  })
}

const mouseenter = function (node) {
  node.showExtra = true
}
const mouseleave = function (node) {
  node.showExtra = false
}

const handleCheck = (node) => {
  if (node.isLeaf) {
    tree.value.setChecked(node.key, !node.checked, false);
  }
};

</script>

<style
  scoped>
  .container {
    display: flex;
    height: 100vh;
    background-color: #f5f7fa;
  }

  .left {
    display: flex;
    flex-direction: column;
    width: 400px;
    padding: 20px;
    box-sizing: border-box;
    background-color: #fff;
    border-radius: 4px;
    /* margin-right: 20px; */
  }

  .tree-wrapper {
    flex: 1;
    overflow-y: auto;
    margin-top: 20px;
  }

  .right {
    flex: 1;
    overflow: hidden;
    background-color: #fff;
    border-radius: 4px;
    padding: 20px;
    box-sizing: border-box;
  }

  .showIcon {
    display: none;
  }

  /deep/ .el-tree-node__content {
    margin-top: 0px;
    transition: background-color 0.3s;
  }

  /deep/ .el-tree-node__content:hover {
    background-color: #f0f2f5;
  }

  /deep/ .el-tree-node__content:hover .showIcon {
    display: block;
  }

  .custom-tree-node {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 8px 0;
  }

  .delete-button {
    height: var(--el-tree-node-content-height);
    border-radius: 0%;
    padding: 0;
    width: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0px;
    transition: background-color 0.3s;
  }

  .delete-button:hover {
    background-color: #ff4d4f;
    color: #fff;
  }

  .button-group {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .el-button {
    margin-left: 10px;
  }

  .el-button--primary {
    background-color: #1890ff;
    border-color: #1890ff;
  }

  .el-button--primary:hover {
    background-color: #40a9ff;
    border-color: #40a9ff;
  }

  .el-button--info {
    background-color: #909399;
    border-color: #909399;
  }

  .el-button--info:hover {
    background-color: #a6a9ad;
    border-color: #a6a9ad;
  }

  .node-content {
    display: flex;
    align-items: center;
  }
  .node-checkbox {
    margin-right: 5px; /* Adjust as needed */
  }
</style>