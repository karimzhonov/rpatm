<template>
  <div class="layout-footer" style="background: #ffffff;">
    <span class="font-medium ml-2">{{ $t('departament_number') }}</span>
  </div>
</template>
<script>
import {useI18n} from "vue-i18n";

export default {
  name: 'AppFooter',
  setup() {
    const {t} = useI18n()
    return {t}
  }
}
</script>

<style lang="scss" scoped></style>
