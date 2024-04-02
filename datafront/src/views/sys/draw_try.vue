<template>
  <div class="container">
    <div class="left">
      <el-button type="primary" style="margin:10px 0px;" @click="getChecked">选中节点图像</el-button>
      <div class="tree-wrapper">
        <el-tree :props="props" ref="tree" :load="loadNode" lazy :key="componentKey" node-key="id" :indent="16"
          @node-click="handleNodeClick"> <template #default="{ node, data }">
            <div class="custom-tree-node" :class="{ 'selected-leaf': selectedLeaves.includes(data) }"> <span
                class="node-label"> <i :class="getNodeIcon(node)"></i> {{ node.label }} </span> <span
                class="node-actions">
                <el-button v-show="node.showExtra" type="danger" :icon="Delete" size="small"
                  @click.stop="remove(node, data)"></el-button>
              </span> </div>
          </template> </el-tree>
      </div>
    </div>
    <div class="right">
      <GraphViewer :graph-info="graph_info" />
    </div>
  </div>
</template>

<script>
import { Delete } from '@element-plus/icons-vue'
import { json2vNG } from '@/util/graph.js';
import GraphViewer from '@/components/GraphViewer.vue';
import { ref } from 'vue'
import { getfirData, getsecData, getthrData, getfouData, getfivData, darwgeo, delnode } from '@/util/base.js'
import { ElMessage, ElMessageBox } from 'element-plus'
const props = {
  label: 'title',
  isLeaf: 'isleaf',
}
const tree = ref('')
const componentKey = ref(0)
const graph_info = ref();
const selectedLeaves = ref([]);
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
      newres.push({
        name: item.name,
        isleaf: true,
        title: item.title,
        relate: item.relate
      })
    }
  })
  return resolve(newres);
}
const loadNode = (node, resolve) => {
  console.log('调用了', node)
  switch (node.level) {
    case 0:
      loadfirstnode(resolve)
      break
    case 1:
      loadsecnode(node, resolve);
      break
    case 2:
      loadthrnode(node, resolve);
      break
    case 3:
      loadfounode(node, resolve);
      break
    case 4:
      loadfivnode(node, resolve);
      break
    default: break
  }
}
const handleNodeClick = (data, node) => {
  if (node.isLeaf) {
    const index = selectedLeaves.value.indexOf(data);
    if (index === -1) {
      selectedLeaves.value.push(data);
    } else {
      selectedLeaves.value.splice(index, 1);
    }
  }
}
const getChecked = async function () {
  if (selectedLeaves.value.length === 0) {
    ElMessage({
      message: '请选择叶子节点',
      type: 'error',
    })
    return
  }
  if (selectedLeaves.value.length > 2) {
    ElMessage({
      message: '最多选择两个叶子节点！！！！',
      type: 'error',
    })
    return
  }
  const minLeaf = selectedLeaves.value[0];
  const maxLeaf = selectedLeaves.value[selectedLeaves.value.length - 1];
  let res = await darwgeo([minLeaf, maxLeaf])
  console.log("data:", res.data)
  graph_info.value = json2vNG(res.data);
  console.log("graph_info:", graph_info)
}
const remove = async function (node, data) {
  console.log(data)
  try {
    await ElMessageBox.confirm('确认删除记录?', 'Warning', {
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
      type: 'warning',
    })
    const res = await delnode(data)
    if (res.code === 200) {
      ElMessage({
        message: res.msg,
        type: 'success',
      })
      componentKey.value += 1
    }
  } catch (error) {
    if (error === 'cancel') {
      ElMessage({
        type: 'info',
        message: 'Delete canceled',
      })
    } else {
      ElMessage({
        message: '删除数据异常',
        type: 'error',
      })
    }
  }
}
const getNodeIcon = (node) => {
  if (node.level === 1) return 'el-icon-video-camera'
  if (node.level === 2) return 'el-icon-time'
  if (node.level === 3) return 'el-icon-film'
  if (node.level === 4) return 'el-icon-picture'
  if (node.level === 5) return 'el-icon-chat-line-round'
  return ''
}
</script>

<style scoped>
/* ... 样式部分保持不变 ... */
</style>
