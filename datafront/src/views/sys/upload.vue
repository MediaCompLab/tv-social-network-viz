<template>
	<div style="margin-left:40px;margin-right:40px">
		<!-- 上传器 -->
		<uploader ref="uploaderRef" :options="options" :autoStart="false" :file-status-text="fileStatusText"
			class="uploader-ui" @file-added="onFileAdded" @file-success="onFileSuccess" @file-progress="onFileProgress"
			@file-error="onFileError">
			<uploader-unsupport></uploader-unsupport>
			<uploader-drop>
				<div>
					<uploader-btn id="global-uploader-btn" ref="uploadBtn">Select file
						<i class="el-icon-upload el-icon--right"></i>
					</uploader-btn>
				</div>
			</uploader-drop>
			<uploader-list></uploader-list>
		</uploader>
	</div>
</template>

<script setup>
import { getToken } from '@/util/auth'
import { reactive, ref, onMounted, defineProps, defineEmits } from 'vue';
import SparkMD5 from 'spark-md5';
// import { mergeFile } from '@/api/demo/fileUpload/index';
import { ElMessage } from 'element-plus';
import { mergefile } from '@/util/base.js'
const props = defineProps(['batchno'])
const emit = defineEmits(['changebatch'])
const options = reactive({
	//目标上传 URL，默认POST, import.meta.env.VITE_API_URL = api
	target: "http://localhost:5000/uploadfile",
	// target: import.meta.env.VITE_API_URL + '/uploader/chunk',
	query: {},
	headers: {
		Authorization: getToken()
	},
	//分块大小(单位：字节)
	chunkSize: '2048000',
	//上传文件时文件内容的参数名，对应chunk里的Multipart对象名，默认对象名为file
	// fileParameterName: 'upfile',
	//失败后最多自动重试上传次数
	maxChunkRetries: 3,
	//是否开启服务器分片校验，对应GET类型同名的target URL
	testChunks: true,
	// 服务器分片校验函数
	checkChunkUploadedByResponse: function (chunk, response_msg) {
		let objMessage = JSON.parse(response_msg);
		if (objMessage.skipUpload) {
			return true;
		}
		return (objMessage.uploadedChunks || []).indexOf(chunk.offset + 1) >= 0;
	},
});

const fileStatusText = reactive({
	success: 'upload success',
	error: 'upload error',
	uploading: 'uploading...',
	paused: 'upload paused',
	waiting: 'waiting...',
});
onMounted(() => {
	// console.log(uploaderRef.value, 'uploaderRef.value');
	// console.log(props.batchno)
});
function onFileAdded(file) {
	if (!props.batchno) {
		ElMessage({
			message: 'batch name cannot be empty',
			type: 'error',
		})
		file.cancel()
		return
	}
	computeMD5(file);
}

function onFileProgress(rootFile, file, chunk) {
	console.log(`uploading ${file.name},chunk：${chunk.startByte / 1024 / 1024} ~ ${chunk.endByte / 1024 / 1024}`)
	file.progress(0.28)
}

function onFileSuccess(rootFile, file, response, chunk) {
	file.batchno = props.batchno
	mergefile(file)
		.then((responseData) => {
			if (responseData.code === 305) {
				// console.log('合并操作未成功，结果码');
				console.log('merging failed')
			}
			ElMessage({
				message: responseData.msg,
				type: 'success',
			})
			emit('changebatch', '')
		})
		.catch(function (error) {
			// console.log('合并后捕获的未知异常：' + error);
			console.log('unknown exception after merge: ' + error);
		});
}
function onFileError(rootFile, file, response, chunk) {
	// console.log('上传完成后异常信息：' + response);
	console.log('exception information after upload completion: ' + response);
}

/**
 * 计算md5，实现断点续传及秒传
 * @param file
 */
function computeMD5(file) {
	file.pause();

	//单个文件的大小限制2G
	let fileSizeLimit = 2 * 1024 * 1024 * 1024;
	// console.log('文件大小：' + file.size);
	console.log('file size：' + file.size);
	// console.log('限制大小：' + fileSizeLimit);
	// if (file.size > fileSizeLimit) {
	// 	file.cancel();
	// }

	let fileReader = new FileReader();
	let time = new Date().getTime();
	let blobSlice =
		File.prototype.slice ||
		File.prototype.mozSlice ||
		File.prototype.webkitSlice;
	let currentChunk = 0;
	const chunkSize = 10 * 1024 * 1000;
	let chunks = Math.ceil(file.size / chunkSize);
	let spark = new SparkMD5.ArrayBuffer();
	//由于计算整个文件的Md5太慢，因此采用只计算第1块文件的md5的方式
	let chunkNumberMD5 = 1;

	loadNext();

	fileReader.onload = (e) => {
		spark.append(e.target.result);

		if (currentChunk < chunkNumberMD5) {
			loadNext();
		} else {
			let md5 = spark.end();
			file.uniqueIdentifier = md5;
			file.resume();
			console.log(
				`MD5计算完毕：${file.name} \nMD5：${md5} \n分片：${chunks} 大小:${file.size
				} 用时：${new Date().getTime() - time} ms`
			);
		}
	};

	fileReader.onerror = function () {
		error(`文件${file.name}读取出错，请检查该文件`);
		file.cancel();
	};

	function loadNext() {
		let start = currentChunk * chunkSize;
		let end = start + chunkSize >= file.size ? file.size : start + chunkSize;

		fileReader.readAsArrayBuffer(blobSlice.call(file.file, start, end));
		currentChunk++;
		// console.log('计算第' + currentChunk + '块');
		console.log('Calculating the ' + currentChunk + ' chunk');
	}
}
const uploaderRef = ref();
function close() {
	uploaderRef.value.cancel();
}
function error(msg) {
	console.log(msg, 'msg');
}
</script>

<!-- <style scoped>
.uploader-ui {
	padding: 15px;
	margin: 20px  0;
	font-size: 12px;
	width: 750px;
	font-family: Microsoft YaHei;
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
}
.uploader-ui .uploader-btn {
	margin-right: 4px;
	font-size: 12px;
	border-radius: 3px;
	color: #fff;
	background-color: #409eff;
	border-color: #409eff;
	display: inline-block;
	line-height: 1;
	white-space: nowrap;
}
.uploader-ui .uploader-list {
	max-height: 440px;
	overflow: auto;
	overflow-x: hidden;
	overflow-y: auto;
}
</style> -->

<style
	scoped>
	.uploader-ui {
		padding: 20px;
		margin: 20px 0;
		font-size: 14px;
		width: 750px;
		background-color: #fff;
		border-radius: 4px;
		border: 1px solid #e8e8e8;
		/* box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); */
	}

	.uploader-ui .uploader-btn {
		margin-right: 10px;
		font-size: 14px;
		border-radius: 4px;
		color: #fff;
		background-color: #1890ff;
		border-color: #1890ff;
		display: inline-block;
		line-height: 1.5;
		white-space: nowrap;
		padding: 6px 15px;
		transition: all 0.3s;
	}

	.uploader-ui .uploader-btn:hover {
		background-color: #40a9ff;
		border-color: #40a9ff;
	}

	.uploader-ui .uploader-list {
		max-height: 440px;
		overflow: auto;
		overflow-x: hidden;
		overflow-y: auto;
		margin-top: 20px;
		border: 1px solid #e8e8e8;
		border-radius: 4px;
	}

	:deep(.uploader-file) {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 10px;
		border-bottom: 1px solid #e8e8e8;
		transition: background-color 0.3s;
	}

	:deep(.uploader-file):last-child {
		border-bottom: none;
	}

	:deep(.uploader-file):hover {
		background-color: #f5f5f5;
	}

	:deep(.uploader-file-progress) {
		flex: 1;
		margin: 0 20px;
	}

	:deep(.uploader-file-name) {
		margin-right: 20px;
		color: #333;
	}

	:deep(.uploader-file-size) {
		margin-left: 20px;
		color: #999;
	}

	:deep(.uploader-file-status) {
		color: #999;
	}

	:deep(.uploader-file-actions) {
		display: flex;
		align-items: center;
	}

	:deep(.uploader-file-actions > div) {
		margin-left: 10px;
		cursor: pointer;
		color: #1890ff;
	}

	:deep(.uploader-file-actions > div:hover) {
		color: #40a9ff;
	}
</style>