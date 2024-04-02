<!-- GraphViewer.vue -->
<!-- <script setup>
import { reactive, computed, ref, watch } from 'vue';
import * as vNG from "v-network-graph";

const props = defineProps({
  graphInfo: Object,
});

const localGraphInfo = reactive(props.graphInfo || {
  nodes: [],
  edges: [],
  layouts: {},
});


const graph = ref(null);
const tooltip = ref(null);
const targetNodeId = ref("");
const tooltipOpacity = ref(0);
const tooltipPos = ref({ left: "0px", top: "0px" });

const zoomLevel = ref(1.5)

const configs = reactive(
  vNG.defineConfigs({
    view: {
      scalingObjects: true,
      minZoomLevel: 0.1,
      maxZoomLevel: 16,
    },
    node: {
      label: {
        visible: true,
        fontFamily: undefined,
        fontSize: 1,
        lineHeight: 1.1,
        color: "#000000",
        margin: 4,
        direction: "south",
        text: "name",
      },
      normal: {
        type: "circle",
        radius: node => node.size,
        color: node => node.color,
      },
      hover: {
        radius: node => node.size + 5,
        color: node => node.color.replace(/(?<=,)[^,]+(?=\))/, "0.5"),
      },
      selectable: true,
      label: {
        visible: node => !!node.label,
      },
      focusring: {
        color: "darkgray",
      },
    },
    edge: {
      normal: {
        width: edge => edge.width,
        color: edge => edge.color,
        dasharray: edge => (edge.dashed ? "4" : "0"),
      },
    },
  })
);

const targetNodePos = computed(() => {
  if (localGraphInfo.layouts.nodes && targetNodeId.value) {
    const nodePos = localGraphInfo.layouts.nodes[targetNodeId.value];
    return nodePos || { x: 0, y: 0 };
  }
  return { x: 0, y: 0 };
});

watch(
  () => props.graphInfo,
  (newGraphInfo) => {
    if (newGraphInfo) {
      Object.assign(localGraphInfo, newGraphInfo);
    }
  },
  { deep: true }
);

watch(
  () => [targetNodePos.value, tooltipOpacity.value],
  () => {
    if (!graph.value || !tooltip.value) return;
    if (targetNodePos.value) {
      const domPoint = graph.value.translateFromSvgToDomCoordinates(targetNodePos.value);
      const currentNode = localGraphInfo.nodes[targetNodeId.value];
      const nodeSize = currentNode ? currentNode.size : 10;
      tooltipPos.value = {
        left: domPoint.x - tooltip.value.offsetWidth / 2 + "px",
        top: domPoint.y - nodeSize - tooltip.value.offsetHeight - 10 + "px",
      };
    }
  },
  { deep: true }
);

const eventHandlers = {
  "node:pointerover": ({ node }) => {
    targetNodeId.value = node;
    tooltipOpacity.value = 1;
  },
  "node:pointerout": () => {
    tooltipOpacity.value = 0;
  },
};
</script> -->

<!-- <template>
  <div class="tooltip-wrapper">
    <v-network-graph
      v-if="localGraphInfo.nodes && localGraphInfo.edges"
      ref="graph"
      v-model:zoom-level="zoomLevel"
      v-model:layouts="localGraphInfo.layouts"
      :nodes="localGraphInfo.nodes"
      :edges="localGraphInfo.edges"
      :configs="configs"
      :event-handlers="eventHandlers"
      v-model:tooltipPos="tooltipPos"
    />
    <div ref="tooltip" class="tooltip" :style="{ ...tooltipPos, opacity: tooltipOpacity }">
      <div>Count: {{ localGraphInfo.nodes[targetNodeId]?.count || 0 }}</div>
    </div>
  </div>
</template> -->

<!-- <style scoped>
.tooltip-wrapper {
  position: relative;
}

.tooltip {
  top: 0;
  left: 0;
  opacity: 0;
  position: absolute;
  width: 80px;
  height: 36px;
  display: grid;
  place-content: center;
  text-align: center;
  font-size: 12px;
  background-color: #fff0bd;
  border: 1px solid #ffb950;
  box-shadow: 2px 2px 2px #aaa;
  color: black;
  transition: opacity 0.2s linear;
  pointer-events: none;
}

.tooltip-wrapper {
  width: 100%;
  height: 100%;
  /* border: 1px solid #000; */
}
</style> -->

<!-- GraphViewer.vue -->
<script setup>
import { reactive, computed, ref, watch, toRaw } from 'vue';
import * as vNG from "v-network-graph";

const props = defineProps({
  graphInfo: Object,
});

const localGraphInfo = reactive(props.graphInfo || {
  nodes: [],
  edges: [],
  layouts: {},
});

const graph = ref(null);
const tooltip = ref(null);
const targetNodeId = ref("");
const targetEdgeId = ref("");
const tooltipOpacity = ref(0);
const tooltipPos = ref({ left: "0px", top: "0px" });
const zoomLevel = ref(1.5);

const EDGE_MARGIN_TOP = 2;

const configs = reactive(
  vNG.defineConfigs({
    view: {
      scalingObjects: true,
      minZoomLevel: 0.1,
      maxZoomLevel: 16,
    },
    node: {
      label: {
        visible: true,
        fontFamily: undefined,
        fontSize: 1,
        lineHeight: 1.1,
        color: "#000000",
        margin: 4,
        direction: "south",
        text: "name",
      },
      normal: {
        type: "circle",
        radius: node => node.size,
        color: node => node.color,
      },
      hover: {
        radius: node => node.size + 5,
        color: node => node.color.replace(/(?<=,)[^,]+(?=\))/, "0.5"),
      },
      selectable: true,
      label: {
        visible: node => !!node.label,
      },
      focusring: {
        color: "darkgray",
      },
    },
    edge: {
      normal: {
        width: edge => edge.width,
        color: edge => edge.color,
        dasharray: edge => (edge.dashed ? "4" : "0"),
      },
    },
  })
);

const targetNodePos = computed(() => {
  if (localGraphInfo.layouts.nodes && targetNodeId.value) {
    const nodePos = localGraphInfo.layouts.nodes[targetNodeId.value];
    return nodePos || { x: 0, y: 0 };
  }
  return { x: 0, y: 0 };
});

const edgeCenterPos = computed(() => {
  const edge = localGraphInfo.edges[targetEdgeId.value];
  if (!edge) return { x: 0, y: 0 };

  console.log("edge.source", edge.source);
  const sourceNode = localGraphInfo.layouts.nodes[edge.source];
  const targetNode = localGraphInfo.layouts.nodes[edge.target];
  return {
    x: (sourceNode.x + targetNode.x) / 2,
    y: (sourceNode.y + targetNode.y) / 2,
  };
});

watch(
  () => props.graphInfo,
  (newGraphInfo) => {
    if (newGraphInfo) {
      Object.assign(localGraphInfo, newGraphInfo);
    }
  },
  { deep: true }
);

watch(
  () => [targetNodePos.value, edgeCenterPos.value, tooltipOpacity.value],
  () => {
    if (!graph.value || !tooltip.value) return;
    if (targetNodeId.value) {
      const domPoint = graph.value.translateFromSvgToDomCoordinates(targetNodePos.value);
      const currentNode = localGraphInfo.nodes[targetNodeId.value];
      const nodeSize = currentNode ? currentNode.size : 10;
      tooltipPos.value = {
        left: domPoint.x - tooltip.value.offsetWidth / 2 + "px",
        top: domPoint.y - nodeSize - tooltip.value.offsetHeight - 10 + "px",
      };
    } else if (targetEdgeId.value) {
      const domPoint = graph.value.translateFromSvgToDomCoordinates(edgeCenterPos.value);
      tooltipPos.value = {
        left: domPoint.x - tooltip.value.offsetWidth / 2 + "px",
        top: domPoint.y - EDGE_MARGIN_TOP - tooltip.value.offsetHeight - 10 + "px",
      };
    }
  },
  { deep: true }
);

const eventHandlers = {
  "node:pointerover": ({ node }) => {
    targetNodeId.value = node;
    tooltipOpacity.value = 1;
  },
  "node:pointerout": () => {
    targetNodeId.value = "";
    tooltipOpacity.value = 0;
  },
  "edge:pointerover": ({ edge }) => {
    targetEdgeId.value = edge;
    tooltipOpacity.value = 1;
  },
  "edge:pointerout": () => {
    targetEdgeId.value = "";
    tooltipOpacity.value = 0;
  },
};
</script>

<template>
  <div class="tooltip-wrapper">
    <v-network-graph
      v-if="localGraphInfo.nodes && localGraphInfo.edges"
      ref="graph"
      v-model:zoom-level="zoomLevel"
      v-model:layouts="localGraphInfo.layouts"
      :nodes="localGraphInfo.nodes"
      :edges="localGraphInfo.edges"
      :configs="configs"
      :event-handlers="eventHandlers"
    />
    <!-- Tooltip -->
    <div ref="tooltip" class="tooltip" :style="{ ...tooltipPos, opacity: tooltipOpacity }">
      <div v-if="targetNodeId">Count: {{ localGraphInfo.nodes[targetNodeId]?.count || 0 }}</div>
      <div v-else-if="targetEdgeId">Freq: {{ localGraphInfo.edges[targetEdgeId]?.count || "" }}</div>
    </div>
  </div>
</template>

<style scoped>
.tooltip-wrapper {
  position: relative;
}
.tooltip {
  top: 0;
  left: 0;
  opacity: 0;
  position: absolute;
  width: 80px;
  height: 36px;
  display: grid;
  place-content: center;
  text-align: center;
  font-size: 12px;
  background-color: #fff0bd;
  border: 1px solid #ffb950;
  box-shadow: 2px 2px 2px #aaa;
  color: black;
  transition: opacity 0.2s linear;
  pointer-events: none;
}
.tooltip-wrapper {
  width: 100%;
  height: 100%;
  /* border: 1px solid #000; */
}
</style>