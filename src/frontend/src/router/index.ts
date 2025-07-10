import { createMemoryHistory, createRouter } from 'vue-router'

import CalendarView from '../views/CalendarView.vue'
import DocumentView from '../views/DocumentView.vue'

const router = createRouter ({
  routes: [
    {
      path: '/', component: CalendarView,
    },
    {
      path: '/document/:name', component: DocumentView
    }
  ],
  history: createMemoryHistory()
})

export default router
