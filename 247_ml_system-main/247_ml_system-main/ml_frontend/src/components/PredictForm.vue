<template>
    <div>
        <el-form ref="formRef" :model="form" :inline="true" size="large" :label-position="'left'" label-width="100px">
            <h3>Predicted output:</h3>
            <el-form-item label="ACCNUM">
                <el-input v-model="form.ACCNUM" type="number"></el-input>
            </el-form-item>
            <el-form-item label="YEAR">
                <el-input v-model="form.YEAR" type="number"></el-input>
            </el-form-item>
            <el-form-item label="TIME">
                <el-input v-model="form.TIME" type="number"></el-input>
            </el-form-item>
            <el-form-item label="HOUR">
                <el-input v-model="form.HOUR" type="number"></el-input>
            </el-form-item>
            <el-form-item label="LATITUDE">
                <el-input v-model="form.LATITUDE" type="number"></el-input>
            </el-form-item>
            <el-form-item label="LONGITUDE">
                <el-input v-model="form.LONGITUDE" type="number"></el-input>
            </el-form-item>
            <el-form-item label="HOOD_ID">
                <el-input v-model="form.HOOD_ID" type="number"></el-input>
            </el-form-item>
            <el-form-item label="WEEKDAY">
                <el-input v-model="form.WEEKDAY" type="number"></el-input>
            </el-form-item>
            <el-form-item label="DAY">
                <el-input v-model="form.DAY" type="number"></el-input>
            </el-form-item>
            <el-form-item label="MONTH">
                <el-input v-model="form.MONTH" type="number"></el-input>
            </el-form-item>
            <el-form-item :label="item" v-for="item in cat_title">
                <el-select :placeholder="item" v-model="form[item]">
                    <el-option :label="att_value" :value="att_value" v-for="att_value in cat_attribute[item]" />
                </el-select>
            </el-form-item>
        </el-form>
        <el-button type="primary" plain @click="submitForm(formRef)">Submit</el-button>

    </div>
</template>

<script lang="ts">
import { FormInstance, FormRules, ElMessage } from 'element-plus'
import { ref } from 'vue'
import { defineComponent } from 'vue'
import ModelService from '@/services/ModelService'
import ResponseData from '@/types/ResponseData';
export default defineComponent({
    name: "predict-form",
    setup() {
        const formRef = ref<FormInstance>()

        return {
            formRef
        }
    },
    props: {
        modelName: String
    },
    data() {
        return {
            form: {
                "ACCNUM": 1300176,
                "YEAR": 2012,
                "TIME": 2016,
                "HOUR": 20,
                "ROAD_CLASS": "Minor Arterial",
                "DISTRICT": "Toronto and East York",
                "LATITUDE": 43.643445,
                "LONGITUDE": -79.43779,
                "LOCCOORD": "Mid-Block",
                "ACCLOC": "Other",
                "TRAFFCTL": "No Control",
                "VISIBILITY": "Rain",
                "LIGHT": "Dusk, artificial",
                "RDSFCOND": "Wet",
                "IMPACTYPE": "Pedestrian Collisions",
                "INVTYPE": "Driver",
                "INVAGE": "30 to 34",
                "VEHTYPE": "Automobile, Station Wagon",
                "PEDESTRIAN": "Yes",
                "CYCLIST": "No",
                "AUTOMOBILE": "Yes",
                "MOTORCYCLE": "No",
                "TRUCK": "No",
                "TRSN_CITY_VEH": "No",
                "EMERG_VEH": "No",
                "PASSENGER": "No",
                "SPEEDING": "No",
                "AG_DRIV": "Yes",
                "REDLIGHT": "No",
                "ALCOHOL": "No",
                "DISABILITY": "No",
                "HOOD_ID": 86,
                "WEEKDAY": 3,
                "DAY": 21,
                "MONTH": 6

            } as any,
            cat_attribute: {} as any,
            cat_title: ['ROAD_CLASS', 'DISTRICT', 'LOCCOORD', 'ACCLOC', 'TRAFFCTL',
                'VISIBILITY', 'LIGHT', 'RDSFCOND', 'IMPACTYPE', 'INVTYPE', 'INVAGE',
                'VEHTYPE', 'PEDESTRIAN', 'CYCLIST', 'AUTOMOBILE', 'MOTORCYCLE', 'TRUCK',
                'TRSN_CITY_VEH', 'EMERG_VEH', 'PASSENGER', 'SPEEDING', 'AG_DRIV', 'REDLIGHT',
                'ALCOHOL', 'DISABILITY']
        }
    },
    methods: {
        getCatAttribute: function () {
            ModelService.getCatAtt().then((res: ResponseData) => {
                this.cat_attribute = res.data;
                // console.log(this.cat_attribute);
            })
                .catch((e: Error) => {
                    console.log(e);
                });
        },
        //submit form
        submitForm: async function (formEl: FormInstance | undefined) {
            if (!formEl) return;
            await formEl.validate((valid, fields) => {
                if (valid && this.$props.modelName) {
                    console.log(this.$props.modelName);
                    console.log(this.form);
                    ModelService.getPredict(this.form, this.$props.modelName).then((res: ResponseData) => {
                        console.log(res.data);
                        if (res.data.prediction.includes('0')) {
                            ElMessage({
                                showClose: true,
                                message: `${this.modelName} Prediction result: non-fatal`,
                                type: 'success',
                            });
                        } else {
                            ElMessage({
                                showClose: true,
                                message: `${this.modelName} Prediction result: fatal`,
                                type: 'warning',
                            });
                        }
                    })
                        .catch((e: Error) => {
                            console.log(e);
                        })
                        ;
                }
            });
        }
    },
    mounted() {
        this.getCatAttribute();
    }
});
</script>