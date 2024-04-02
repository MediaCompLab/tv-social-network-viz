<!-- <template>
<el-container class="layout-container-demo" style="height: 100%">
    <el-aside width="200px">
        <el-scrollbar>
            <el-menu active-text-color="#409eff" :default-active="route.path" :router="true" class="el-menu-vertical-demo" :default-openeds="['1']">
                <el-sub-menu index="1">
                    <template #title>
                        <el-icon>
                            <setting />
                        </el-icon>Graph demo
                    </template>
                    <el-menu-item index="/tranfile">Upload file</el-menu-item>
                    <el-menu-item index="/draw">Graph display</el-menu-item>
                </el-sub-menu>
            </el-menu>
        </el-scrollbar>
    </el-aside>

    <el-container>
        <el-header style="text-align: right; font-size: 12px;">
            <div class="toolbar">
                <el-dropdown>
                    <el-icon style="margin-right: 8px; margin-top: 1px">
                        <setting />
                    </el-icon>
                    <template #dropdown>
                        <el-dropdown-menu>

                            <el-dropdown-item @click="logout">Exit</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </div>
        </el-header>

        <el-main>
            <el-scrollbar>
                <router-view v-slot="{ Component }">
                    <keep-alive>
                        <component :is="Component" :key="$route.name" v-if="$route.meta.keepAlive" />
                    </keep-alive>
                    <component :is="Component" :key="$route.name" v-if="!$route.meta.keepAlive" />
                </router-view>
            </el-scrollbar>
        </el-main>
    </el-container>
</el-container>
</template> -->

<template>
  <el-container class="layout-container-demo" style="height: 100%">
    <el-aside width="200px">
      <el-scrollbar>
        <el-menu active-text-color="#409eff" :default-active="route.path" :router="true" class="el-menu-vertical-demo"
          :default-openeds="['1']">
          <el-sub-menu index="1">
            <template #title>
              <el-icon>
                <setting />
              </el-icon>Graph demo
            </template>
            <el-menu-item index="/tranfile">Upload file</el-menu-item>
            <el-menu-item index="/draw">Graph display</el-menu-item>
          </el-sub-menu>
        </el-menu>
        <div class="logout-btn-wrapper">
          <el-button type="danger" @click="logout">Exit</el-button>
        </div>
      </el-scrollbar>
    </el-aside>
    <el-container>
      <el-main>
        <el-scrollbar>
          <router-view v-slot="{ Component }">
            <keep-alive>
              <component :is="Component" :key="$route.name" v-if="$route.meta.keepAlive" />
            </keep-alive>
            <component :is="Component" :key="$route.name" v-if="!$route.meta.keepAlive" />
          </router-view>
        </el-scrollbar>
      </el-main>
    </el-container>
  </el-container>
</template>



<script setup>
import { ref, onMounted } from 'vue'
import { apiverify } from '@/util/base.js'
import Cookies from 'js-cookie'
import { Document, Menu as IconMenu, Setting } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import { removeToken } from '@/util/auth.js'

const route = useRoute()
const router = useRouter()

function logout() {
  removeToken()
  Cookies.remove('flask_token')
  router.push('/login')
}
onMounted(async () => {
  await apiverify()
}
)
</script>

<!-- <style scoped>
* {
  font-family: 'Arial', sans-serif;
}

.layout-container-demo .el-header {
  position: relative;
  background-color: var(--el-color-primary-light-7);
  color: var(--el-text-color-primary);
}

.layout-container-demo .el-aside {
  color: var(--el-text-color-primary);
  background: var(--el-color-primary-light-8);

}

.layout-container-demo .el-menu {
  border-right: none;
}

.layout-container-demo .el-main {
  padding: 0;
}

.layout-container-demo .toolbar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  right: 20px;
}

.el-menu,
.el-menu-item {
  background-color: #D9ECFF;
}

/deep/ .el-scrollbar__view {
  height: 100%;
}

.logout-btn-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.logout-btn-wrapper .el-button {
  width: 100%;
}
</style> -->

<style scoped>
  *{
    font-family: 'Arial', sans-serif;
  }
  .layout-container-demo .el-aside {
    background-color: #f0f2f5;
    color: #333;
  }

  .layout-container-demo .el-menu {
    background-color: #e4e7ed;
    border-right: none;
  }

  .layout-container-demo .el-sub-menu__title,
  .layout-container-demo .el-menu-item {
    background-color: #e4e7ed;
    color: #333;
    font-family: 'Arial', sans-serif;
  }

  .layout-container-demo .el-menu-item.is-active {
    background-color: #ffffff;
    color: #000000;
  }

  .layout-container-demo .el-main {
    padding: 0;
  }

  .logout-btn-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    background-color: #f0f2f5;
  }

  .logout-btn-wrapper .el-button {
    width: 100%;
  }
</style>