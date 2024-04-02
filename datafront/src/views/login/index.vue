<!-- sign_up -->
<template>
    <div class="login">
        <h1 class="title">Graph demo</h1>
        <div class="main">
            <div class="user">username:<input type="text" id="username" v-model="username"></div>
            <div class="pwd">password:<input type="password" id="password" v-model="password"></div>
        </div>
        <div class="footer">
            <el-button type="success" @click="logi">login</el-button>
            <router-link to="/register"><el-button type="primary"> register </el-button></router-link>

        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { login } from '@/util/base.js'
import { useRouter } from 'vue-router'
import { setToken } from '@/util/auth.js'
const router = useRouter()
let username = ref('')
let password = ref('')
const logi = async function () {
    if (!username.value || !password.value) {
        ElMessage.error('username or password cannot be empty')
        return
    } else {
        await login({ 'username': username.value, 'password': password.value }).then(
            (res) => {
                if (res.code == 200) {
                    ElMessage({
                        message: 'login successfully, will jump to the home page soon',
                        type: 'success',
                    })
                    console.log(res)
                    setToken(res.token)
                    setTimeout(() => {
                        router.push('/')
                    }, 1000);
                }
                else {
                    ElMessage({
                        message: 'login failed',
                        type: 'error',
                    })
                }
            }
        ).catch(error => {
            console.log(error)
        })
    }
}

</script>

<!-- <style scoped>
 
*{
    margin: 0;
    padding: 0;
    font-family: 'Arial', sans-serif;
}
body{
    background-color: lightgrey;
}
.login{
    position: absolute;
    top: 50%;
    left: 50%;
    height: 220px;
    width: 500px;
    border: 1px solid darkgray;
    border-radius: 10px;
    transform: translate(-50%,-50%);
}
.title{
    margin:20px 0;
    text-align: center;
}
#username,#password{
    height:30px;
    width: 220px;
    margin-top: 10px;
}
.main {
    text-align: center;
}
.footer{
    text-align: center;
}
.el-button{
    margin: 10px 10px;
    height: 30px;
    width: 50px;
    outline: none;
}
.el-button a{
    text-decoration: none;
}
</style> -->
<style
    scoped>
    * {
        margin: 0;
        padding: 0;
        font-family: 'Arial', sans-serif;
    }

    body {
        background-color: #f5f5f5;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }

    .login {
        background-color: #fff;
        border-radius: 10px;
        padding: 30px;
        width: 400px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    .title {
        color: #333;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
    }

    .main {
        margin-bottom: 20px;
        text-align: center;
    }

    .user,
    .pwd {
        margin-bottom: 10px;
    }

    #username,
    #password {
        height: 30px;
        width: 220px;
        margin-left: 10px;
        padding: 5px;
        border: 1px solid #ccc;
        border-radius: 3px;
    }

    .footer {
        text-align: center;
    }

    .el-button {
        margin: 10px;
        height: 30px;
        padding: 0 15px;
        border: none;
        border-radius: 3px;
        cursor: pointer;
    }

    .el-button[type="success"] {
        background-color: #28a745;
        color: #fff;
    }

    .el-button[type="primary"] {
        background-color: #007bff;
        color: #fff;
    }
</style>