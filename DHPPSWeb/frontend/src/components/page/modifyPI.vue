<template>
  <!-- 实现了生日日期选择，没有实现输入框校验！！！ -->
  <div id="app">
    <div class="layui-layout layui-layout-admin">
      <div class="layui-header">
        <div class="layui-logo">LOGO</div>
        <div class="layui-logotext">高传染性疾病预测系统</div>
        <!-- <div class="layui-logo">高传染性疾病预测系统</div> -->
        <!-- 头部区域（可配合layui已有的水平导航） -->
        <ul class="layui-nav layui-layout-left">
          <li class="layui-nav-item">个人中心</li>
        </ul>
        <ul class="layui-nav layui-layout-right">
          <li class="layui-nav-item" style="line-height: 40px">
            <router-link
              style="margin-left: 10px; float: left"
              :to="{
                path: '/setting',
                query: {
                  params: JSON.stringify({
                    userId: this.userId,
                    casename: 999,
                  }),
                },
              }"
              >回到首页</router-link
            >
          </li>
          <li class="layui-nav-item" style="line-height: 20px">
            <el-avatar
              shape="circle"
              :size="30"
              :fit="fit"
              :src="url"
            ></el-avatar>
          </li>
          <li class="layui-nav-item">
            <a href="javascript:;">
              <span>{{ content.username }}</span>
            </a>
          </li>
        </ul>
      </div>
      <div class="layui-side layui-bg-black">
        <div class="layui-side-scroll">
          <!-- 左侧导航区域（可配合layui已有的垂直导航） -->
          <ul class="layui-nav layui-nav-tree" lay-filter="test">
            <li class="layui-nav-item layui-nav-itemed">
              <div
                style="
                  text-align: center;
                  background-color: #fff;
                  font-size: 16px;
                  color: rgb(132, 132, 136);
                "
              >
                <i
                  class="layui-icon layui-icon-app"
                  style="font-size: 20px; color: rgb(173, 173, 173)"
                ></i>
                系统菜单
              </div>
              <dl class="layui-nav-child">
                <dd>
                  <router-link
                    :to="{ path: '/profile', query: { userId: userId } }"
                    >个人资料</router-link
                  >
                </dd>
              </dl>
              <router-link
                :to="{ path: '/modifyPI', query: { userId: userId } }"
                >修改资料</router-link
              >
              <dl class="layui-nav-child">
                <dd>
                  <router-link
                    :to="{ path: '/caseView', query: { userId: userId } }"
                    >案例查看</router-link
                  >
                </dd>
              </dl>
            </li>
          </ul>
        </div>
      </div>
      <div class="layui-body">
        <!-- 内容主体区域 -->
        <div style="padding: 15px">
          <div class="layui-tab layui-tab-brief" lay-filter="docDemoTabBrief">
            <ul class="layui-tab-title">
              <li class="layui-this" style="color: #55587e">修改资料</li>
              <li>
                <router-link
                  :to="{ path: '/changePass', query: { userId: userId } }"
                  style="color: #55587e"
                  >修改密码</router-link
                >
              </li>
            </ul>
            <div class="layui-tab-content">
              <div class="list">
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
                        :src="url"
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
                  <el-form-item label="手机号" prop="phone">
                    <el-input
                      size="small"
                      v-model="ruleForm.phone"
                      clearable
                      id="inputphone"
                    ></el-input>
                  </el-form-item>
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
                    <el-button type="primary" @click="submitForm('ruleForm')"
                      >保存</el-button
                    >
                    <el-button class="reset" @click="resetForm('ruleForm')"
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
</template>

<script src="layui.js"></script>
<script>
export default {
  name: "modifyPI",
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
    return {
      userId: this.$route.query.userId,
      sex: "",
      // 获取信息
      content: [],
      // 头像
      input: "",
      // 头像
      fits: ["fill"],
      url:
        "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
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
        phone: "",
        email: "",
        radio: "男",
        delivery: false,
        type: [],
        addr: "",
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
      },
    };
  },
  created: function () {
    //为了在内部函数能使用外部函数的this对象，要给它赋值了一个名叫self的变量。
    // alert(this.userId)
    this.getContent();
  },
  methods: {
    changeHandler(value) {
      this.sex = value;
    },
    getContent: function () {
      var self = this;
      axios
        .get("http://127.0.0.1:8000/backend/profile/" + this.userId + "/")
        .then(
          (response) =>
            (self.content = response.data)
            // alert(JSON.stringify(response))
        )
        .catch(function (error) {
          // 请求失败处理.
          // alert("数据请求失败wdnmd");
        });
    },
    putContent: function (userId) {
      var self = this;
      var uname = $("#inputname").val();
      axios
        .put("http://127.0.0.1:8000/backend/profile/" + userId + "/", {
          username: $("#inputname").val(),
          phonenumber: $("#inputphone").val(),
          birth: this.value1,
          sex: this.ruleForm.radio,
          email: $("#inputmail").val(),
          address: $("#inputaddr").val(),
        })
        .then(
          (response) => (
            (self.content = response),
            // alert("数据发送"),
            this.$message.success("修改成功"),
            this.$router.push({
              path: "/profile",
              query: {
                  userId: this.userId
              },
            })
            // alert(JSON.stringify(response))
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
  },
};
</script>

<style scoped>
@import "../../assets/layui/css/layui.css";
.list {
  text-align: center;
  margin: 10px 300px;
}
/* 表单 */
.el-form {
  text-align: center;
}
.el-form-item {
  margin-top: 20px;
  width: 320px;
}

/* el按钮 */
.el-button {
  margin-top: 30px;
  background: #55587e;
  border: 0px;
  width: 80px;
  height: 30px;
}
.reset {
  background: #fff;
  border: 1px #55587e solid;
}
.el-checkbox :hover {
  background: #8b9bbd;
}

/* 左侧导航栏 */
/* 第一个hover */
.layui-nav-tree .layui-nav-item a {
  font-weight: bold;
  background-color: rgb(131, 137, 158);
}
.layui-nav-tree .layui-nav-item a:hover {
  background-color: #55587e;
}
/* 第二三块的字体 */
.layui-nav-tree .layui-nav-child a {
  height: 40px;
  line-height: 40px;
  font-weight: normal;
  background-color: #fff;
  color: rgba(10, 12, 22, 0.411);
}
/* 第二三块的背景 */
.layui-nav-itemed > .layui-nav-child {
  display: block;
  padding: 0;
  background-color: rgba(212, 187, 187, 0.966);
}
/* 第二三块的hover */
.layui-nav .layui-nav-child a:hover {
  background-color: #55587e;
  color: rgb(255, 255, 255);
}
/* LOGO */
.layui-layout-admin .layui-logo {
  position: absolute;
  left: 0;
  top: 0;
  width: 200px;
  height: 50%;
  line-height: 40px;
  text-align: center;
  color: #ffffff;
}
.layui-layout-admin .layui-logotext {
  position: absolute;
  left: 0;
  top: 0;
  width: 200px;
  height: 50%;
  line-height: 80px;
  text-align: center;
  color: #ffffff;
  font-size: 10px;
  font-size: 10px;
}
.layui-layout-admin .layui-header {
  background-color: #8b9bbd;
}
.layui-side-scroll {
  position: relative;
  width: 220px;
  height: 100%;
  overflow-x: hidden;
  background-color: #ffffff;
}
/* 选项卡 */
.layui-tab-brief {
  color: #61637c;
}
.layui-tab-title {
  color: #61637c;
}
.layui-tab-brief > .layui-tab-more li.layui-this:after,
.layui-tab-brief > .layui-tab-title .layui-this:after {
  border: none;
  border-radius: 0;
  border-bottom: 2px solid rgb(245, 152, 65);
}
.layui-this {
  color: #55587e;
  font-weight: bold;
}
.layui-form-label {
  text-align: left;
  width: 45px;
}
/* 按钮 */
.layui-btn {
  background-color: #55587e;
}
.layui-btn-primary {
  background-color: #fff;
}
</style>
