import DefaultTheme from 'vitepress/theme'
import Layout from './Layout.vue'
import AiPickArticle from './components/AiPickArticle.vue'
import AiPickCover from './components/AiPickCover.vue'
import AiPickReferenceList from './components/AiPickReferenceList.vue'
import AiPickSummaryGrid from './components/AiPickSummaryGrid.vue'
import './ai-open-source-picks.css'
import './custom.css'

export default {
  extends: DefaultTheme,
  Layout: Layout,
  enhanceApp({ app }) {
    app.component('AiPickArticle', AiPickArticle)
    app.component('AiPickCover', AiPickCover)
    app.component('AiPickSummaryGrid', AiPickSummaryGrid)
    app.component('AiPickReferenceList', AiPickReferenceList)
  },
}
