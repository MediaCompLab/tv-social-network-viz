<template>
        <el-row>
          <div class="el-upload__tip text-red" style="margin-left: 40px;color: red;">
        First enter the batch name, verify it, and then select the file to upload
      </div>
        </el-row>
        <el-row>
          <span style="margin-left: 40px;vertical-align: bottom;line-height: 32px;">batch name:</span><el-col :span="10"><el-input v-model="form.batchno" style="vertical-align: top;" placeholder="batch name must be unique" @blur="bnouni"/></el-col>
      </el-row>
      <upload :batchno="form.batchno" @changebatch="updatebno"></upload>
      
</template>

<script setup lang="ts">
import upload from '@/views/sys/upload.vue'
import { ref,reactive } from 'vue'
import  {  unibno } from "@/util/base";
import { ElMessage } from 'element-plus'
const form = reactive({
    batchno: '',
})
let elref=ref('')

const bnouni=async function () {
  await unibno({'batchno':form.batchno}).then(res=>{
    console.log(res)
    if(res.code===305){
    ElMessage({
              message: res.msg,
              type: 'error',
            })
            form.batchno=''
  }


  }).catch(error=>{
    console.log(error)
  }
  )
  
}
function updatebno(){
  form.batchno=''
}

</script>

<style scoped>
.main{
    margin: 10px 40px;
    display: flex;
}
.left,.right{
  flex:1
}
#btn1{
    margin-left: 40px;
}

.el-form {
  margin-top: 40px;
}
.upload{
    margin-top: 30px;
    margin-left:30px;
    margin-bottom: 30px;
}
#submit{
    display: flex;
    justify-content: center;
    align-items: center;
}
#submit .el-button:first-child{
    margin-left: 270px;
}

.el-input{
    padding-left: 10px;
}
.el-row{
  margin: 20px 0;
  width: 100%;
  padding-right: 30px;
}
</style>