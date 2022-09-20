<template>
    <div>
        <el-row :gutter="12">
            <el-col :span="8">
                <el-card shadow="hover" @click="handleSelectModel('Logistic_Regression')">
                    <div class="card-content">Logistic Regression</div>
                </el-card>
            </el-col>
            <el-col :span="8">
                <el-card shadow="hover" @click="handleSelectModel('Decision_Tree')">
                    <div class="card-content">Decision Tree</div>
                </el-card>
            </el-col>
            <el-col :span="8">
                <el-card shadow="hover" @click="handleSelectModel('SVM')">
                    <div class="card-content">Support Vector Machine</div>
                </el-card>
            </el-col>
        </el-row>
        <el-divider />
        <el-row :gutter="12">
            <el-col :span="6">
                <el-progress type="dashboard" :percentage="Number((stat.accuracy * 100).toFixed(1))">
                    <template #default="{ percentage }">
                        <span class="percentage-value">{{ percentage }}%</span>
                        <span class="percentage-label">Accuracy</span>
                    </template>
                </el-progress>
            </el-col>
            <el-col :span="6">
                <el-progress type="dashboard" :percentage="Number((stat.f1 * 100).toFixed(1))">
                    <template #default="{ percentage }">
                        <span class="percentage-value">{{ percentage }}%</span>
                        <span class="percentage-label">F1</span>
                    </template>
                </el-progress>
            </el-col>
            <el-col :span="6">
                <el-progress type="dashboard" :percentage="Number((stat.precision * 100).toFixed(1))">
                    <template #default="{ percentage }">
                        <span class="percentage-value">{{ percentage }}%</span>
                        <span class="percentage-label">Precision</span>
                    </template>
                </el-progress>
            </el-col>
            <el-col :span="6">
                <el-progress type="dashboard" :percentage="Number((stat.recall * 100).toFixed(1))">
                    <template #default="{ percentage }">
                        <span class="percentage-value">{{ percentage }}%</span>
                        <span class="percentage-label">Recall</span>
                    </template>
                </el-progress>
            </el-col>
        </el-row>
        <el-divider />
        <el-row>
            <el-col>
                <el-card shadow="always">
                    <el-descriptions title="Metric Score">
                        <el-descriptions-item label="Model Name">{{ modelName }}</el-descriptions-item>
                        <el-descriptions-item label="Accuracy">{{ stat.accuracy }}</el-descriptions-item>
                        <el-descriptions-item label="Precision">{{ stat.precision }}</el-descriptions-item>
                        <el-descriptions-item label="Recall">{{ stat.recall }}</el-descriptions-item>
                        <el-descriptions-item label="F1">{{ stat.f1 }}</el-descriptions-item>
                    </el-descriptions>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ModelService from '@/services/ModelService'
import ResponseData from '@/types/ResponseData';

export default defineComponent({
    setup() {
    },
    data() {
        return {
            "modelName": 'SVM',
            "stat": {
                "accuracy": 0.9542052744119743,
                "f1": 0.9553276551364506,
                "precision": 0.9324737020699015,
                "recall": 0.9793300071275838
            }
        }
    },
    methods: {
        getScore: function (modelName: string) {
            ModelService.getScores(modelName).then((res: ResponseData) => {
                this.stat.accuracy = res.data.accuracy;
                this.stat.f1 = res.data.f1;
                this.stat.precision = res.data.precision;
                this.stat.recall = res.data.recall;
                console.log(res.data);
            })
                .catch((e: Error) => {
                    console.log(e);
                })
                ;
        },
        handleSelectModel: function (modelName: string) {
            this.modelName = modelName;
        }
    },
    mounted() {
        this.getScore(this.modelName);
    },
    watch: {
        modelName(newName, oldName) {
            console.log(`from watch` + newName);
            this.getScore(newName);
        },
        stat(newStat) {
            this.stat = newStat;
        }
    }
});
</script>

<style>
.title-circle {
    text-align: center;
}

.percentage-value {
    display: block;
    margin-top: 10px;
    font-size: 28px;
}

.percentage-label {
    display: block;
    margin-top: 10px;
    font-size: 12px;
}

.demo-progress .el-progress--line {
    margin-bottom: 15px;
    width: 350px;
}

.demo-progress .el-progress--circle {
    margin-right: 15px;
}
</style>