<template>
  <div style="background-color: rgb(235, 234, 250)">
    <div class="wrapper">
      <!-- Sidebar  -->
      <div class="iq-sidebar" style="z-index: 1">
        <div class="iq-sidebar-logo d-flex justify-content-between">
          <span style="font-size: 18px">高传染性疾病预测系统</span>
        </div>
        <div id="sidebar-scrollbar">
          <nav class="iq-sidebar-menu">
            <ul class="iq-menu" style="margin-top: 20px">
              <li>
                <router-link
                  class="iq-waves-effect"
                  :to="{
                    path: '/UserProfile',
                    query: { uI: this.AdminId },
                  }"
                  ><i class="ri-profile-line"></i
                  ><span>个人资料</span></router-link
                >
              </li>
              <li class="active">
                <a class="iq-waves-effect"
                  ><i class="ri-file-edit-line"></i><span>修改资料</span></a
                >
              </li>
              <li>
                <router-link
                  class="iq-waves-effect"
                  :to="{
                    path: '/UserCase',
                    query: { uI: this.AdminUserId },
                  }"
                  ><i class="ri-file-list-line"></i
                  ><span>我的案例</span></router-link
                >
              </li>
            </ul>
          </nav>
          <div class="p-3"></div>
        </div>
      </div>

      <!-- TOP Nav Bar -->
      <div class="iq-top-navbar" style="z-index: 1">
        <div class="iq-navbar-custom">
          <!-- <div class="iq-sidebar-logo">
               <div class="top-logo">
                  <a href="index.html" class="logo">
                  <img src="images/logo.gif" class="img-fluid" alt="">
                  <span>vito</span>
                  </a>
               </div>
            </div> -->
          <nav class="navbar navbar-expand-lg navbar-light p-0">
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
              <ul class="navbar-nav ml-auto navbar-list">
                <li class="nav-item">
                  <a class="search-toggle iq-waves-effect" href="#"
                    ><i class="ri-calendar-line"></i
                  ></a>
                  <div class="iq-sub-dropdown">
                    <div class="calender-small"></div>
                  </div>
                </li>
              </ul>
            </div>
            <ul class="navbar-list">
              <li>
                <a
                  href="#"
                  class="search-toggle iq-waves-effect d-flex align-items-center"
                >
                  <img
                    :fit="fit"
                    :src="Url"
                    class="img-fluid rounded mr-3"
                    alt="user"
                  />
                  <div class="caption">
                    <h6 class="mb-0 line-height">{{ MyContent.userName }}</h6>
                  </div>
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
      <!-- TOP Nav Bar END -->
      <!-- Page Content  -->
      <div id="content-page" class="content-page" style="z-index: 1">
        <div class="container-fluid">
          <div class="row">
            <div class="col-lg-12" v-if="!show">
                     <div class="iq-card">
                        <div class="iq-card-body p-0">
                           <div class="iq-edit-list">
                              <ul class="iq-edit-profile d-flex nav nav-pills">
                                 <li class="col-md-6 p-0">
                                    <a class="nav-link active" data-toggle="pill">
                                       修改资料
                                    </a>
                                 </li>
                                 <li class="col-md-6 p-0">
                                    <a class="nav-link" data-toggle="pill" @click="ShowEditPWD()">
                                       修改密码
                                    </a>
                                 </li>
                              </ul>
                           </div>
                        </div>
                     </div>
                  </div>

            <div class="col-lg-6" style="left:25%" v-if="!show">
              <div class="iq-edit-list-data">
                <div class="tab-content">
                  <div
                    class="tab-pane fade active show"
                    id="personal-information"
                    role="tabpanel"
                  >
                    <div class="iq-card">
                      <div
                        class="iq-card-body"
                        style="padding-right: 30px; padding-left: 30px"
                      >
<el-form
                  :model="ruleForm"
                  :rules="rules"
                  :label-position="labelPosition"
                  ref="ruleForm"
                  label-width="100px"
                  class="demo-ruleForm"
                >
                  <div class="demo-fit" style="text-align: center">
                    <div class="block">
                      <el-avatar
                        shape="circle"
                        :size="70"
                        :fit="fill"
                        :src="Url"
                      ></el-avatar>
                    </div>
                  </div>
                  <el-form-item label="昵称" prop="name">
                    <el-input
                      size="small"
                      v-model="ruleForm.name"
                      clearable
                      id="inputname"
                    ></el-input>
                  </el-form-item>
                  <!-- <el-form-item label="手机号" prop="phone">
                    <el-input
                      size="small"
                      v-model="ruleForm.phone"
                      clearable
                      id="inputphone"
                    ></el-input>
                  </el-form-item> -->
                  <el-form-item label="性别" prop="sex">
                    <el-radio-group
                      v-model="ruleForm.radio"
                      @change="changeHandler"
                      id="inputsex"
                    >
                      <el-radio label="男"></el-radio>
                      <el-radio label="女"></el-radio>
                      <el-radio label="保密"></el-radio>
                    </el-radio-group>
                  </el-form-item>
                  <el-form-item label="生日">
                    <el-date-picker
                      clearable
                      v-model="value1"
                      type="date"
                      value-format="yyyy-MM-dd"
                      placeholder="选择日期"
                      size="small"
                      style="
                        margin-left: 0;
                        align: left;
                        display: block;
                        float: left;
                      "
                      id="inputdate"
                    >
                    </el-date-picker>
                  </el-form-item>
                  <el-form-item label="邮箱" prop="email">
                    <el-input
                      size="small"
                      v-model="ruleForm.email"
                      clearable
                      id="inputmail"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="住址" prop="addr">
                    <el-input
                      size="small"
                      v-model="ruleForm.addr"
                      clearable
                      id="inputaddr"
                    ></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button class="btn btn-primary mr-2" @click="submitForm('ruleForm')"
                      >保存</el-button
                    >
                    <el-button class="btn iq-bg-danger" @click="resetForm('ruleForm')"
                      >重置</el-button
                    >
                  </el-form-item>
                </el-form>

                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

<div class="col-lg-12" v-if="show">
                     <div class="iq-card">
                        <div class="iq-card-body p-0">
                           <div class="iq-edit-list">
                              <ul class="iq-edit-profile d-flex nav nav-pills">
                                 <li class="col-md-6 p-0">
                                    <a class="nav-link" data-toggle="pill" @click="CloseEditPWD()">
                                       修改资料
                                    </a>
                                 </li>
                                 <li class="col-md-6 p-0">
                                    <a class="nav-link active" data-toggle="pill">
                                       修改密码
                                    </a>
                                 </li>
                              </ul>
                           </div>
                        </div>
                     </div>
                  </div>
            <div class="col-lg-6" style="left:25%" v-if="show">
              <div class="iq-edit-list-data">
                <div class="tab-content">
                  <div
                    class="tab-pane fade active show"
                    id="personal-information"
                    role="tabpanel"
                  >
                    <div class="iq-card">
                      <div
                        class="iq-card-body"
                        style="padding-right: 30px; padding-left: 30px"
                      >
                        <el-form
                  :model="ruleForm"
                  :rules="rules"
                  :label-position="labelPosition"
                  ref="ruleForm"
                  label-width="100px"
                  class="demo-ruleForm"
                >
                  <el-form-item
                    label="原密码"
                    prop="prePass"
                    style="margin-top: 50px"
                  >
                    <el-input
                      type="password"
                      placeholder="请输入原密码"
                      v-model="ruleForm.prePass"
                      autocomplete="off"
                      id="prepass"
                    ></el-input>
                  </el-form-item>
                  <el-form-item
                    label="新密码"
                    prop="pass"
                    style="margin-top: 50px"
                  >
                    <el-input
                      type="password"
                      placeholder="请输入新密码"
                      v-model="ruleForm.pass"
                      autocomplete="off"
                      id="newpass"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="确认新密码" prop="checkPass"
                      style="margin-top: 50px">
                    <el-input
                      type="password"
                      placeholder="请再次输入新密码"
                      v-model="ruleForm.checkPass"
                      autocomplete="off"
                    ></el-input>
                  </el-form-item>
                  <el-form-item>
                      
                    <el-button class="btn btn-primary mr-2" @click="PWDsubmitForm('ruleForm')"
                      >保存</el-button
                    >
                    <el-button class="btn iq-bg-danger" @click="PWDresetForm('ruleForm')"
                      >重置</el-button
                    >
                  </el-form-item>
                </el-form>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    var checkanme = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("请输入昵称"));
      }
      setTimeout(() => {
        let reg = /^[(a-zA-Z0-9\u4e00-\u9fa5){1}_#]{1,20}$/;
        if (value == "" || !reg.test(value)) {
          callback(
            new Error("昵称限1-20个字符，支持中英文、数字、减号或下划线")
          );
        } else {
          callback();
        }
      });
    };
    var checkphone = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("请输入手机号"));
      }
      setTimeout(() => {
        let reg = /^1[0-9]{10}$/;
        if (value == "" || value.length < 11 || !reg.test(value)) {
          callback(new Error("请输入正确的手机号"));
        } else {
          callback();
        }
      });
    };
    var checkemail = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("请输入邮箱"));
      }
      setTimeout(() => {
        let reg = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
        if (value == "" || !reg.test(value)) {
          callback(new Error("请输入正确的邮箱"));
        } else {
          callback();
        }
      });
    };
    var validatePass= (rule, value, callback) => {
        if (!value) {
          return callback(new Error('请输入密码'));
        }
        setTimeout(() => {
          let reg =  /^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[._~!@#$^&*])[A-Za-z0-9._~!@#$^&*]{6,12}$/
          if (value == '' || !reg.test(value)) {
            callback(new Error('密码长度为6~12位，必须由字母、数字、特殊符号(._~!@#$^&*)组成'));
          }
          else{
            callback();
          }
        });
      }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== this.ruleForm.pass) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    return {
      show: false,
      // 头像
      fits: ["fill"],
      Url:
        "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
      MyContent: [],
      AdminId: "46",
      sex: "",
      // 设置单选默认值
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now();
        },
      },
      labelPosition: "left",
      value1: "",
      ruleForm: {
        name: "",
        // phone: "",
        email: "",
        radio: "男",
        delivery: false,
        type: [],
        addr: "",

        prePass: "",
        pass: "",
        checkPass: "",
      },
      rules: {
        name: [{ required: true, validator: checkanme, trigger: "blur" }],
        phone: [{ required: true, validator: checkphone, trigger: "blur" }],
        email: [{ required: true, validator: checkemail, trigger: "change" }],
        type: [
          {
            type: "array",
            required: true,
            message: "请选择一个选项",
            trigger: "change",
          },
        ],
        addr: [{ required: true, trigger: "change" }],
        sex: [{ required: false, trigger: "change" }],
        addr: [{ min: 0, max: 50 }],

        prePass: [{ required: true, validator: validatePass, trigger: "blur" }],
        pass: [{ required: true, validator: validatePass, trigger: "blur" }],
        checkPass: [
          { required: true, validator: validatePass2, trigger: "change" },
        ],
      },
      passMassege: "", //获取原密码是否正确的信息
    };
  },
  created: function () {
    this.getMyContent(), this.getUserContent();
  },
  methods: {
    getMyContent: function () {
      var self = this;
      axios
        .get("/apis/backend/profile/25/")
        .then(
          (response) => (
            (self.MyContent = response.data),
            (this.Url = self.MyContent.avatar)
          )
        )
        .catch(function (error) {
          // 请求失败处理
          alert("数据请求失败wdnmd");
        });
    },
    putContent: function (userId) {
      var self = this;
      var uname = $("#inputname").val();
      alert($("#inputname").val());
      axios
        .put("/apis/backend/profile/25/", {
          userName: $("#inputname").val(),
          // phonenumber: $("#inputphone").val(),
          birth: this.value1,
          sex: this.ruleForm.radio,
          email: $("#inputmail").val(),
          address: $("#inputaddr").val(),
        })
        .then(
          (response) => (
            (self.content = response),
            this.$message.success("修改成功")
          )
        )
        .catch(function (error) {
          // alert(JSON.stringify(response))
          // alert("数据发送失败")
          console.log(error.response);
        });
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.putContent(this.userId);
          // alert('submit!')
        } else {
          this.$message.error("修改失败");
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    submitMessage: function () {
      if (this.passMassege == "账号原密码错误") {
        this.$message.error("原密码错误");
      } else if (this.passMassege == "修改成功") {
        this.$message.success("修改密码成功");
      } else {
        this.$message.error("修改失败");
      }
    },
    changePass: function () {
      var self = this;
      let data = new FormData();
      data.append("userId", 46);
      data.append("oldPassword", $("#prepass").val());
      data.append("newPassword", $("#newpass").val());
      // var prepass=$("#prepass").val()
      axios
        .post("/apis/backend/changePwd/", data)
        .then(
          (response) => (
            (self.content = response.data),
            (self.passMassege = response.data.message),
            // alert(JSON.stringify(response.data.message)),
            // self.$message.success("修改密码成功")
            self.submitMessage()
          )
        )
        .catch(function (error) {
          // 请求失败处理
          alert(JSON.stringify(error.response));
          alert("数据请求失败wdnmd");
        });
    },
    PWDsubmitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // alert("this is submit")
          this.changePass();
          // this.putContent()
          // alert('submit!')
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    PWDresetForm(formName) {
      this.$refs[formName].resetFields();
    },
    ShowEditPWD(){
      this.show=true;
    },
    CloseEditPWD() {
      this.show=false;
    }
  },
};
</script>

<style>
@import "../../css/bootstrap.min.css";
@import "../../css/typography.css";
@import "../../css/style.css";
@import "../../css/animate.css";
</style>