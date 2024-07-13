<script>

import axios from 'axios';
import FAQSection from './components/FAQSection.vue';

export default {
    components: {
        FAQSection
    },
    data() {
        return {
            newJob: {
                name: '',
                jobTitle: '',
                steps: []
            },
            jobs: [],
            editingIndex: -1
        };
    },
    mounted() {
        this.fetchJobs();
    },
    methods: {
        fetchJobs() {
        // get all jobs
        axios.get('http://127.0.0.1:5000/api/jobs')
            .then(response => {
                this.jobs = response.data;
                expanded: false
            })
            .catch(error => {
                console.error('Error fetching jobs:', error);
                alert('Failed to fetch jobs. Please refresh the page.');
            });
        },
        toggleJob(index) {
            this.jobs[index].expanded = !this.jobs[index].expanded;
        },
        addStep() {
            this.newJob.steps.push({
                stepDesc: '',
                haz: [{ 
                    hazDesc: '', 
                    mit: ['']
                }]
            });
        },
        addHaz(stepIndex) {
            this.newJob.steps[stepIndex].haz.push({
                hazDesc: '',
                mit: ['']
            });
        },
        addMit(stepIndex, hazIndex) {
            this.newJob.steps[stepIndex].haz[hazIndex].mit.push('');
        },
        removeStep(index) {
            this.newJob.steps.splice(index, 1);
        },
        removeHaz(stepIndex, hazIndex) {
            this.newJob.steps[stepIndex].haz.splice(hazIndex, 1);
        },
        removeMit(stepIndex, hazIndex, mitIndex) {
            this.newJob.steps[stepIndex].haz[hazIndex].mit.splice(mitIndex, 1);
        },
        submitJob() {
            if (this.newJob.steps.length > 0) {
                axios.post('http://127.0.0.1:5000/api/jobs', this.newJob)
                .then(response => {
                    this.fetchJobs(); // refetch jobs
                    this.clearForm(); // empty form
                    alert('Job added successfully');
                })
                .catch(error => {
                    console.error('Error adding job:', error);
                    alert('Failed to add job');
                });
            } else {
                alert('Please add at least one step.');
            }
        },
        editJob(index) {
            if (this.editingIndex == index) {
                this.clearForm(); // undo autofill
            } else {
                // autofill form with preexisting JHA
                const selectedJob = this.jobs[index];

                this.newJob.name = selectedJob.name;
                this.newJob.jobTitle = selectedJob.jobTitle;
                this.newJob.steps = selectedJob.steps.map(step => {
                    return {
                        stepDesc: step.stepDesc,
                        haz: step.haz.map(haz => {
                            return {
                                hazDesc: haz.hazDesc,
                                mit: haz.mit.map(mitigation => mitigation.mitDesc)
                            };
                        })
                    };
                });
                this.editingIndex = index;
            }
        },
        updateJob() {
            if (this.editingIndex > -1) {
                axios.put(`http://127.0.0.1:5000/api/jobs/${this.jobs[this.editingIndex].id}`, this.newJob)
                .then(response => {
                    console.log('Job updated successfully:', response.data);
                    this.fetchJobs(); // refetch
                    this.clearForm(); // empty form
                    this.editingIndex = -1; // reset edit index
                    alert('Job updated successfully');
                })
                .catch(error => {
                    console.error('Error updating job:', error);
                    alert('Failed to update job');
                });
            }
        },
        deleteJob(id) {
            if (confirm('Are you sure you want to delete this job?')) {
                axios.delete(`http://127.0.0.1:5000/api/jobs/${id}`)
                .then(() => {
                    this.jobs = this.jobs.filter(job => job.id !== id);
                    this.fetchJobs(); // refetch
                    this.clearForm(); // empty form
                    alert(`Job ${id} deleted successfully`);
                })
                .catch(error => {
                    console.error('error deleting job:', error);
                    alert('Failed to delete job. Please try again.');
                });
            }
        },
        clearForm() {
            this.newJob.name = '';
            this.newJob.jobTitle = '';
            this.newJob.steps = [];
            this.editingIndex = -1;
        }
    }
};
</script>


<template>
    <div class="px-5 py-5 my-3 mx-auto text-center bg-light">
      <h1 class="display-5 fw-bold">Acme Widgets, Inc.</h1>
      <h1 class="display-4 fw-bold py-3">Job Hazard Analysis Page</h1>
      <div class="col-lg-6 mx-auto">
            <p class="lead mb-4">A new, digitized JHA process. Create your own JHA's, and view existing JHA's from other Acme Widget employees.</p>
        </div>
    </div>

    <div class="container-fluid">
        <div class="row">
            <div class="col-6">
                <h2 class="my-3 text-center">Create a Job Hazard Analysis</h2>
                <!-- add new job or update existing job -->
                <form @submit.prevent="editingIndex === -1 ? submitJob() : updateJob()">

                    <div class="row">
                        <div class="form-group">
                            <div class="row">
                                <div class="col-6">
                                    <label>Full Name</label>
                                    <input name="name" type="text" v-model="newJob.name" class="form-control" required>
                                </div>
                                <div class="col-6">
                                    <label>Job Title</label>
                                    <input name="jobTitle" type="text" v-model="newJob.jobTitle" class="form-control" required>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div style="height: 20px;"></div>
            
                    <!-- dynamic fields -->
                    <div v-for="(step, stepIndex) in newJob.steps" :key="stepIndex" class="card mb-3">
                        <div class="card-header">
                            <h5 class="mt-1 text-center">Step {{ stepIndex + 1 }} Attributes</h5>
                        </div>
                        <div class="card-body">
                            <div class="form-group">
                                <label>Description</label>
                                <textarea v-model="step.stepDesc" class="form-control" rows="3" required></textarea>
                            </div>

                            <div style="height: 10px;"></div>
                            <hr>   
                            <div style="height: 10px;"></div>

                            <div v-for="(haz, hazIndex) in step.haz" :key="hazIndex" class="card mb-2">
                                <div class="card-header">
                                    <h6 class="mt-3 ms-2">Hazard {{ hazIndex + 1 }}
                                        <span style="float:right;">
                                            <button type="button" class="btn btn-danger btn-sm float-end mb-2" @click="removeHaz(stepIndex, hazIndex)">Remove Hazard</button>
                                        </span>
                                    </h6>
                                </div>
                                <div class="card-body">
                                    <div class="form-group">
                                        <label>Description</label>
                                        <textarea v-model="haz.hazDesc" class="form-control" rows="2" required></textarea>
                                    </div>
                                    
                                    <div style="height: 30px;"></div>

                                    <div v-for="(mit, mitIndex) in haz.mit" :key="mitIndex" class="form-group">
                                        <label>Mitigation {{ mitIndex + 1 }}</label>
                                        <div class="row">
                                            <div class="col-10">
                                                <textarea v-model="haz.mit[mitIndex]" class="form-control" rows="2" required></textarea>
                                            </div>
                                            <div class="col-2">
                                                <button type="button" class="btn-close btn-sm float-end mt-3 me-2" @click="removeMit(stepIndex, hazIndex, mitIndex)"></button>
                                            </div>
                                        </div>
                                    </div>

                                    <div style="height: 10px;"></div>
                                    <div class="text-center">
                                        <button type="button" class="btn btn-secondary mt-2" @click="addMit(stepIndex, hazIndex)">Add Mitigation</button>
                                    </div>
                                </div>
                            </div>

                            <button type="button" class="btn btn-secondary me-2 mt-2" @click="addHaz(stepIndex)">Add Hazard</button>
                            <button type="button" class="btn btn-danger mt-2" @click="removeStep(stepIndex)">Remove Step</button>
                        </div>
                    </div>

                    <div class="col-sm-offset-3 col-sm-9">
                        <!-- add step -->
                        <button type="button" class="btn btn-primary me-2 mb-2" @click="addStep">Add Step</button>
                        <!-- cool button that changes label whether you are adding new job or editing existing job -->
                        <button type="submit" class="btn btn-success mb-2" :disabled="newJob.steps.length === 0">{{ editingIndex === -1 ? 'Submit JHA' : 'Update JHA' }}</button>
                    </div>

                </form>

                <div style="height: 10px;"></div>
                <hr>   
                <div style="height: 10px;"></div>

            <!-- FAQ -->
            <FAQSection />
            
            </div>

            <div class="col-6">
                <!-- submitted jobs -->
                <div class="mx-2 text-center">
                    <h2 class="my-3 mb-4">Submitted JHA's</h2>
                    <div v-for="(job, index) in jobs" :key="index" class="card mb-3">
                        
                        <div class="card-header">
                            <h3 class="my-3"><strong>{{ job.jobTitle }}</strong></h3>
                            <h6 class="mt-4" style="text-align:left;">Submitted by {{ job.name }}
                                <span style="float:right;">
                                    <button class="btn btn-sm btn-warning me-2 mb-1" @click="editJob(index)">Edit</button>
                                    <button class="btn btn-sm btn-danger mb-1" @click="deleteJob(job.id)">Delete</button>
                                </span>
                            </h6>
                        </div>

                        <ul class="list-group list-group-flush">
                            <li class="list-group-item" v-for="(step, sIndex) in job.steps" :key="sIndex">
                                <h5 class="mt-1"><strong>Step {{ sIndex + 1 }}: </strong>{{ step.stepDesc }}</h5>
                                <div v-for="(hazard, hIndex) in step.haz" :key="hIndex">
                                    <hr>
                                    <h6 class="mb-3"><strong>Hazard {{ hIndex + 1 }}: </strong>{{ hazard.hazDesc }}</h6>
                                    <p><strong>Mitigations: </strong></p>
                                    <div class="container">
                                        <div v-for="(mitigation, mIndex) in hazard.mit" :key="mIndex">
                                            <p style="line-height:1.0;">- {{ mitigation.mitDesc }}</p>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        </ul>

                    </div>
                </div>
            </div>
        </div>
    </div>

    <div style="height: 60px;"></div>
    
  </template>