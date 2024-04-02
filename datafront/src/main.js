import '@/assets/css/global.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from '@/router'
import * as echarts from "echarts";
import uploader from 'vue-simple-uploader';
import 'vue-simple-uploader/dist/style.css';

import VNetworkGraph from "v-network-graph"
import "v-network-graph/lib/style.css"

createApp(App).use(ElementPlus).use(router).use(echarts).use(uploader).use(VNetworkGraph).mount('#app')