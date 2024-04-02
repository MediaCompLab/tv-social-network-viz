<template>
    <div class="timeline-tree">
      <div v-for="(node, index) in timelineData" :key="index" class="timeline-node">
        <div class="node-label" @click="toggleExpand(node)">
          <i :class="getNodeIcon(node)"></i>
          {{ node.label }}
          <i v-if="node.children && node.children.length" :class="node.expanded ? 'el-icon-arrow-down' : 'el-icon-arrow-right'"></i>
        </div>
        <div v-if="node.expanded" class="node-children">
          <div v-for="(child, childIndex) in node.children" :key="childIndex" class="timeline-node">
            <div v-if="!child.isLeaf" class="node-label" @click="toggleExpand(child)">
              <i :class="getNodeIcon(child)"></i>
              {{ child.label }}
              <i v-if="child.children && child.children.length" :class="child.expanded ? 'el-icon-arrow-down' : 'el-icon-arrow-right'"></i>
            </div>
            <div v-else class="node-label leaf-node" :class="{ 'selected-node': child.selected }" @click="selectNode(child)">
              <i :class="getNodeIcon(child)"></i>
              {{ child.label }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const props = defineProps({
    timelineData: {
      type: Array,
      required: true,
    },
  });
  
  const emit = defineEmits(['nodeSelected']);
  
  const toggleExpand = (node) => {
    if (node.children && node.children.length) {
      node.expanded = !node.expanded;
    }
  };
  
  const selectNode = (node) => {
    if (node.isLeaf) {
      node.selected = !node.selected;
      emit('nodeSelected', node);
    }
  };
  
  const getNodeIcon = (node) => {
    if (node.level === 1) return 'el-icon-video-camera';
    if (node.level === 2) return 'el-icon-time';
    if (node.level === 3) return 'el-icon-film';
    if (node.level === 4) return 'el-icon-picture';
    if (node.level === 5) return 'el-icon-chat-line-round';
    return '';
  };
  </script>
  
  <style scoped>
  .timeline-tree {
    position: relative;
    padding-left: 20px;
  }
  
  .timeline-node {
    position: relative;
    margin-bottom: 20px;
  }
  
  .timeline-node::before {
    content: '';
    position: absolute;
    top: 0;
    left: -20px;
    width: 2px;
    height: 100%;
    background-color: #e4e7ed;
  }
  
  .node-label {
    display: flex;
    align-items: center;
    padding: 10px;
    background-color: #f5f7fa;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .node-label i {
    margin-right: 5px;
    color: #c0c4cc;
  }
  
  .leaf-node {
    background-color: #e8f4ff;
  }
  
  .selected-node {
    border: 2px solid red;
  }
  
  .node-children {
    margin-left: 20px;
    padding-left: 20px;
    border-left: 2px solid #e4e7ed;
  }
  </style>