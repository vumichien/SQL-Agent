<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import type { TrainRequest } from '@/types/api'

interface Props {
  visible: boolean
  loading?: boolean
}

withDefaults(defineProps<Props>(), {
  loading: false,
})

const emit = defineEmits<{
  'update:visible': [value: boolean]
  submit: [data: TrainRequest]
}>()

// Active tab
const activeTab = ref<'ddl' | 'documentation' | 'sql'>('sql')

// Form data
const formData = reactive<TrainRequest>({
  ddl: '',
  documentation: '',
  question: '',
  sql: '',
})

// Form refs
const formRef = ref<FormInstance>()

// Form validation rules
const ddlRules: FormRules = {
  ddl: [
    { required: true, message: 'DDL statement is required', trigger: 'blur' },
    { min: 10, message: 'DDL must be at least 10 characters', trigger: 'blur' },
  ],
}

const documentationRules: FormRules = {
  documentation: [
    { required: true, message: 'Documentation is required', trigger: 'blur' },
    { min: 10, message: 'Documentation must be at least 10 characters', trigger: 'blur' },
  ],
}

const sqlRules: FormRules = {
  question: [
    { required: true, message: 'Question is required', trigger: 'blur' },
    { min: 5, message: 'Question must be at least 5 characters', trigger: 'blur' },
  ],
  sql: [
    { required: true, message: 'SQL query is required', trigger: 'blur' },
    { min: 10, message: 'SQL must be at least 10 characters', trigger: 'blur' },
  ],
}

const currentRules = ref<FormRules>(sqlRules)

// Watch active tab to update validation rules
watch(activeTab, (newTab) => {
  if (newTab === 'ddl') {
    currentRules.value = ddlRules
  } else if (newTab === 'documentation') {
    currentRules.value = documentationRules
  } else {
    currentRules.value = sqlRules
  }
})

// Handle dialog close
const handleClose = () => {
  emit('update:visible', false)
  resetForm()
}

// Handle form submit
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    // Prepare data based on active tab
    const submitData: TrainRequest = {}

    if (activeTab.value === 'ddl') {
      submitData.ddl = formData.ddl
    } else if (activeTab.value === 'documentation') {
      submitData.documentation = formData.documentation
    } else {
      submitData.question = formData.question
      submitData.sql = formData.sql
    }

    emit('submit', submitData)
  } catch (error) {
    console.error('Form validation failed:', error)
  }
}

// Reset form
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  formData.ddl = ''
  formData.documentation = ''
  formData.question = ''
  formData.sql = ''
}

// Example templates
const ddlExample = `CREATE TABLE employees (
  id INTEGER PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  department VARCHAR(50),
  salary DECIMAL(10, 2)
);`

const documentationExample = `The employees table stores information about company staff members. Each employee has a unique ID, full name, department assignment, and salary. The salary field uses decimal precision for accurate monetary values.`

const questionExample = `How many employees are in the sales department?`
const sqlExample = `SELECT COUNT(*)
FROM employees
WHERE department = 'sales';`

const insertExample = (type: 'ddl' | 'documentation' | 'question' | 'sql') => {
  if (type === 'ddl') {
    formData.ddl = ddlExample
  } else if (type === 'documentation') {
    formData.documentation = documentationExample
  } else if (type === 'question') {
    formData.question = questionExample
  } else if (type === 'sql') {
    formData.sql = sqlExample
  }
}
</script>

<template>
  <el-dialog
    :model-value="visible"
    title="Add Training Data"
    width="700px"
    :before-close="handleClose"
    :close-on-click-modal="false"
  >
    <el-tabs v-model="activeTab" type="border-card">
      <!-- DDL Tab -->
      <el-tab-pane label="DDL" name="ddl">
        <el-form
          ref="formRef"
          :model="formData"
          :rules="currentRules"
          label-position="top"
          @submit.prevent="handleSubmit"
        >
          <el-form-item label="DDL Statement (CREATE TABLE)" prop="ddl">
            <el-input
              v-model="formData.ddl"
              type="textarea"
              :rows="10"
              placeholder="Enter CREATE TABLE statement..."
              :disabled="loading"
            />
            <div class="form-item-helper">
              <span class="helper-text">Provide table schema definitions</span>
              <el-button
                type="primary"
                link
                size="small"
                @click="insertExample('ddl')"
              >
                Insert Example
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- Documentation Tab -->
      <el-tab-pane label="Documentation" name="documentation">
        <el-form
          ref="formRef"
          :model="formData"
          :rules="currentRules"
          label-position="top"
          @submit.prevent="handleSubmit"
        >
          <el-form-item label="Documentation" prop="documentation">
            <el-input
              v-model="formData.documentation"
              type="textarea"
              :rows="10"
              placeholder="Enter table or column documentation..."
              :disabled="loading"
            />
            <div class="form-item-helper">
              <span class="helper-text">Describe tables, columns, or business rules</span>
              <el-button
                type="primary"
                link
                size="small"
                @click="insertExample('documentation')"
              >
                Insert Example
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- SQL (Q&A) Tab -->
      <el-tab-pane label="SQL (Q&A)" name="sql">
        <el-form
          ref="formRef"
          :model="formData"
          :rules="currentRules"
          label-position="top"
          @submit.prevent="handleSubmit"
        >
          <el-form-item label="Question" prop="question">
            <el-input
              v-model="formData.question"
              placeholder="Enter natural language question..."
              :disabled="loading"
            />
            <div class="form-item-helper">
              <span class="helper-text">Natural language question</span>
              <el-button
                type="primary"
                link
                size="small"
                @click="insertExample('question')"
              >
                Insert Example
              </el-button>
            </div>
          </el-form-item>

          <el-form-item label="SQL Query" prop="sql">
            <el-input
              v-model="formData.sql"
              type="textarea"
              :rows="8"
              placeholder="Enter corresponding SQL query..."
              :disabled="loading"
            />
            <div class="form-item-helper">
              <span class="helper-text">Corresponding SQL query for the question</span>
              <el-button
                type="primary"
                link
                size="small"
                @click="insertExample('sql')"
              >
                Insert Example
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose" :disabled="loading">Cancel</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="loading">
          Add Training Data
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.form-item-helper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 4px;
}

.helper-text {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

/* Tabs styling */
:deep(.el-tabs--border-card) {
  border: 1px solid var(--el-border-color);
  box-shadow: none;
}

:deep(.el-tabs__content) {
  padding: 20px;
}

/* Textarea styling */
:deep(.el-textarea__inner) {
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
  font-size: 13px;
}
</style>
