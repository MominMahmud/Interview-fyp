import api from './environment'

const requests={
    
    createJobs: api + '/createjobs',
    getQuestions:api + '/getQuestions',
    getJobs:api+'/jobs',
    setEmotions:api+'/setEmotions',
    createCandidate:api+'/candidates',
    getCandidateEmail:api+'/getC',
    getQuestionsByJob:api+'/getQuestionsByJob'
}
export default requests