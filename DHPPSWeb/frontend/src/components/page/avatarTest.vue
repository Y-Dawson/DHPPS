<template>
  <div>
    <el-avatar
      shape="circle"
      :size="70"
      :fit="fill"
      :src="imageUrl"
    ></el-avatar>
    <el-upload
      action="#"
      class="upload-demo"
      :show-file-list="false"
      :on-success="handleAvatarSuccess"
      :before-upload="beforeAvatarUpload"
      :on-progress="handleAvatarSuccess"
      style="margin-top:-20px;"
    >
    <div class="avatarEdit" cursor:pointer  style="background: #827af3; margin-top:-20px; padding-bottom:0px;width:30px;padding-top:2px; height:30px;border:0px;color:#fff;border-radius: 50%;text-align:center;">
      <i class="el-icon-edit" style="font-size:18px;margin-bottom:-5px"></i>
    </div>
    <!-- <el-button style="background: #827af3; width:10px;height:10px;border:0px;color:#fff;border-radius: 50%;font-size:14px;text-align:center;">
      <i class="el-icon-edit" style="font-size:18px;"></i>
    </el-button> -->
    <!-- <div style="background: #827af3; color:#fff;border-radius: 50%;width:20px;">
      <i class="ri-pencil-line upload-button"></i>
    </div> -->
    
      <!-- <div class="p-image">
        
        <input class="file-upload" type="file" accept="image/*" />
      </div> -->
      <!-- <img :src="imageUrl" :fit="fit" class="avatar"> -->
      <!-- <i class="el-icon-plus avatar-uploader-icon"></i> -->
    </el-upload>
    <el-button @click="putContent">上传</el-button>
  </div>
</template>


<style>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
.avatarEdit:hover{
  border:0px;
  background-color: #e6ebf3;
}
.avatarEdit:focus{
  border:0px;
}
</style>

<script>
export default {
  data() {
    return {
      imageUrl: "",
      image: "",
    };
  },
  created: function () {
    this.getMyContent();
  },
  methods: {
    getMyContent: function () {
      var self = this;
      axios
        .get("/apis/backend/profile/1/")
        .then((response) => {
          (self.MyContent = response.data),
            (this.imageUrl = self.MyContent.avatar);
          // alter(response.data)
        })
        .catch(function (error) {
          // 请求失败处理
          alert("数据请求失败wdnmd");
        });
    },
    putContent: function (userId) {
      var self = this;
      let data = new FormData();
      data.append("avatar", this.image);
      console.log("现在呢");
      console.log(this.image);
      axios
        .put("/apis/backend/profile/1/", data)
        // .put("/apis/backend/profile/1/", {
        //   avatar:this.image
        //   // userName:"XX"
        // })
        .then((response) => {
          alert(response);
        })
        .catch(function (error) {
          // alert(JSON.stringify(response))
          alert("数据发送失败");
          console.log(error.response);
        });
    },
    handleAvatarSuccess(res, file, fileList) {
      // alert("success")
      this.image = fileList[0].raw;
      console.log("现在的图片是：");
      console.log(file.raw);
      this.imageUrl = URL.createObjectURL(file.raw);
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === "image/jpeg";
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error("上传头像图片只能是 JPG 格式!");
      }
      if (!isLt2M) {
        this.$message.error("上传头像图片大小不能超过 2MB!");
      }
      return isJPG && isLt2M;
    },
  },
};
</script>