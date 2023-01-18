<template>
<div v-if="loading" class="layout-main row justify-content-center">
        <div class="col">
                    <ProgressSpinner style="top:30%; left:47%"/>
                </div>
  </div>
  <div v-if="!loading">
    <BackOrStart :header="$t('Махаллы')" :navigator="[]"/>
    <div class="card mt-3 rounded-4">
      <div class="col-12">
        <div class="row">
          <div class="col">
            <div>
                <data-table filterDisplay="row" v-model:filters="filters" :value="data" showGridlines responsiveLayout="scroll">
                <column field="number" :header="$t('Место')">
                  <template #body="slotProps">
                    <div>{{ data.indexOf(slotProps.data) + 1}}</div>
                  </template>
                </column>
                <column field="sector" :header="$t('Сектор')" :showFilterMenu="false">
                  <template #filter="{filterModel,filterCallback}">
                        <MultiSelect v-model="filterModel.value" :options="sector_list" @change="filterCallback" optionLabel="number" :placeholder="$t('Выберите сектор')" class="p-column-filter">
                            <template #option="slotProps">
                              <span class="image-text">{{`${$t('Сектор')} - ${slotProps.option.number}`}}</span>
                            </template>
                            <template #value="slotProps">
                                {{ slotProps.value ? slotProps.value.reduce((a, v) => [...a, `${$t('Сектор')} - ${v.number}`], []).join(', ') : $t('Выберите сектор') }}
                        </template>
                        </MultiSelect>
                    </template>
                  <template #body="slotProps">
                    <div>{{ `${$t('Сектор')} - ${slotProps.data.sector.number}`}}</div>
                  </template>
                </column>
                <column field="region" :header="$t('Район')" :showFilterMenu="false">
                  <template #body="slotProps">
                    <div>{{ slotProps.data.region.name}}</div>
                  </template>
                  <template #filter="{filterModel, filterCallback}">
                        <MultiSelect v-model="filterModel.value" :options="region_list" @change="filterCallback()" optionLabel="name" :placeholder="$t('Выберите регион')" class="p-column-filter">
                            <template #option="slotProps">
                              <span class="image-text">{{slotProps.option.name}}</span>
                            </template>
                        </MultiSelect>
                    </template>
                </column>
                <column field="area" :header="$t('Махалла')" :showFilterMenu="false">
                  <template #body="slotProps">
                    <div>{{ slotProps.data.area.name}}</div>
                  </template>
                  <template #filter="{filterModel, filterCallback}">
                        <InputText type="text" v-model="filterModel.value" @input="filterCallback()" class="p-column-filter" :placeholder="$t('Поиск по махаллям')"/>
                    </template>
                </column>
                <column field="index" :header="$t('ИЧД')" :showFilterMenu="false" :showClearButton="false" :showFilterMatchModes="false">
                  <template #body="slotProps">
                    <div>{{ slotProps.data.index}}</div>
                  </template>
                  <template #filter=slotProps>
                    <Slider :max="index_range[1]" :min="index_range[0]" :step="0.01" v-model="slotProps.filterModel.value" range class="m-3"></Slider>
                    <div class="flex align-items-center justify-content-between px-2">
                        <span>{{slotProps.filterModel.value ? slotProps.filterModel.value[0] : index_range[0]}}</span>
                        <span>{{slotProps.filterModel.value ? slotProps.filterModel.value[1] : index_range[1]}}</span>
                    </div>
                  </template>
                </column>
              </data-table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import store from '@/store';
import BackOrStart from '@/components/BackOrStart.vue';
import {FilterMatchMode,FilterOperator} from 'primevue/api';

export default {
    name: 'DataTableView',
    components: {BackOrStart},
    async mounted() {
      // Init sector filter
      const sectors = await store.dispatch('fetch_sectors')
      const sectors_id_list = this.$route.query.sector ? this.$route.query.sector.split(',').reduce((a, v) => [...a, parseInt(v)], []) : []
      const filter_sector = []
      for (let sector of sectors) {
        if (sectors_id_list.includes(sector.id)) {
          filter_sector.push(sector)
        }
      }
      this.filters.sector.value = filter_sector.length > 0 ? filter_sector : null
      // Init region filter
      await store.dispatch('fetch_regions')
      await store.dispatch('fetch_data_table', {
        file: this.$route.query.file, 
        index_color: this.$route.query.index_color, 
        main_criteria: true})
      store.commit('basic', {key: 'loading', value: false})
    },
    data() {
      const index_range_list = {
        'red': [0, 0.55],
        'blue': [0.55, 0.65],
        'green': [0.65, 1.00]
      }
      return {
        index_range: index_range_list[this.$route.query.index_color],
        filters: {
          'sector': {value: null, matchMode: FilterMatchMode.IN},
          'region': {value: null, matchMode: FilterMatchMode.IN}, 
          'area': {value: null, constraints: [{value: null, matchMode: FilterMatchMode.CONTAINS}]},
          'index': {value: index_range_list[this.$route.query.index_color], matchMode: FilterMatchMode.BETWEEN},
        }
      }
    },
    computed: {
        data: () => store.state.data_table,
        loading: () => store.state.loading,
        sector_list: () => store.state.sectors,
        region_list: () => store.state.regions,
    },
}
</script>