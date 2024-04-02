<template>
    <div class="register">
        <h2 class="title">Register</h2>
        <div class="main">
            <div>username:<input type="text" id="username" v-model="username"></div>
            <div>password:<input type="password" id="password" v-model="password"></div>
            <div class="pwd">confirm password:<input type="password" id="password2" v-model="password2"></div>
        </div>
        <div class="footer">
            <router-link to="/login" style="text-decoration: none">Have an account, log in</router-link>
            <el-button type="primary" @click="reg">Register</el-button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { register } from '@/util/base.js'
import { useRouter } from 'vue-router'
const router = useRouter()
let username = ref('')
let password = ref('')
let password2 = ref('')
const validatePassword = function (password) {//必须为字母加数字且长度不小于8位
    var str = password;
    if (str == null || str.length < 6) {
        ElMessage({
            message: 'password length must be greater than 6',
            type: 'error',
        })
        return false;
    }
    var reg2 = new RegExp(/^[a-zA-Z][a-zA-Z0-9]{5,15}$|^[0-9][a-zA-Z0-9]{5,15}$/);
    if (reg2.test(str)) {
        return true;
    } else {
        ElMessage({
            message: 'password must be a combination of letters and numbers',
            type: 'error',
        })
        return false;
    }
}
const reg = async function () {
    if (!username.value || !password.value) {
        ElMessage.error('username or password cannot be empty')
        return
    } else {
        if (validatePassword(password.value) && password.value == password2.value) {
            await register({ 'username': username.value, 'password': password.value }).then(
                (res) => {
                    if (res.code == 200) {
                        ElMessage({
                            message: 'register successfully, will jump to the login page soon',
                            type: 'success',
                        })
                        setTimeout(() => {
                            router.push('/login')
                        }, 2000);
                    }
                    else {
                        ElMessage({
                            message: 'register failed',
                            type: 'error',
                        })
                    }
                }
            ).catch(error => {
                console.log(error)
            })
        }
        else {
            ElMessage({
                message: 'password does not match',
                type: 'error',
            })
        }
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
        background-color: lightblue;
    }
    .register{
        position: absolute;
        top: 50%;
        left: 50%;
        height: 300px;
        width: 500px;
        border: 1px solid darkgray;
        border-radius: 10px;
        transform: translate(-50%,-50%);
    }
    .title{
        margin:20px 0;
        text-align: center;
    }
    #username,#password,#password2{
        height:30px;
        width: 220px;
        margin-top: 10px;
    }
    .main {
        text-align: center;
    }
    .footer{
        margin-top: 10px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-decoration: none;
    }
    .el-button{
        margin: 10px 10px;
        height: 30px;
        width: 150px;
        outline: none;
    }
    .pwd{
        text-indent: -2em;
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

    .register {
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
    }

    .main div {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }

    .main div label {
        color: #666;
        margin-right: 10px;
    }

    input {
        width: 250px;
        padding: 5px;
        border: 1px solid #ccc;
        border-radius: 3px;
    }

    .footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 20px;
    }

    .footer a {
        color: #666;
        text-decoration: none;
    }

    .el-button {
        padding: 8px 20px;
        background-color: #007bff;
        color: #fff;
        border: none;
        border-radius: 3px;
        cursor: pointer;
    }
</style>