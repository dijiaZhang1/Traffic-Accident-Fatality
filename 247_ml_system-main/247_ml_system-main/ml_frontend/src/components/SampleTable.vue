<template>
    <div>
        <el-table :data="tableData" style="width: 100%">
            <el-table-column :prop="column" :label="column" width="180" v-for="column in columns" />
        </el-table>
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
            tableData: [],
            columns: ['ACCNUM', 'YEAR', 'TIME', 'HOUR',
                'ROAD_CLASS', 'DISTRICT', 'LATITUDE',
                'LONGITUDE', 'LOCCOORD', 'ACCLOC',
                'TRAFFCTL', 'VISIBILITY', 'LIGHT',
                'RDSFCOND', 'IMPACTYPE', 'INVTYPE',
                'INVAGE', 'VEHTYPE', 'PEDESTRIAN',
                'CYCLIST', 'AUTOMOBILE', 'MOTORCYCLE',
                'TRUCK', 'TRSN_CITY_VEH', 'EMERG_VEH',
                'PASSENGER', 'SPEEDING', 'AG_DRIV',
                'REDLIGHT', 'ALCOHOL', 'DISABILITY',
                'HOOD_ID', 'WEEKDAY', 'DAY', 'MONTH']
        }
    },
    methods: {
        getSampleData: function () {
            ModelService.getSample().then((res: ResponseData) => {
                this.tableData = res.data;
                console.log(this.tableData);
            }).catch((e: Error) => {
                console.log(e);
            });
        }
    },
    mounted() {
        this.getSampleData();
    }
});
</script>