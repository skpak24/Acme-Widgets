<script>

import axios from 'axios';

export default {
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
            })
            .catch(error => {
                console.error('Error fetching jobs:', error);
                alert('Failed to fetch jobs. Please refresh the page.');
            });
        },
        addStep() {
            this.newJob.steps.push({
                description: '',
                hazards: '',
                mitigation: ''
            });
        },
        removeStep(index) {
            this.newJob.steps.splice(index, 1);
        },
        submitJob() {
            if (this.newJob.steps.length > 0) {
                axios.post('http://127.0.0.1:5000/api/jobs', this.newJob)
                .then(response => {
                    console.log('Job added successfully:', response.data);
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
            // fill form with preexisting JHA
            this.newJob.name = this.jobs[index].name;
            this.newJob.jobTitle = this.jobs[index].jobTitle;
            this.newJob.steps = this.jobs[index].steps.map(step => ({ ...step }));
            this.editingIndex = index;
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
                            <input type="text" v-model="newJob.name" class="form-control" required>
                            </div>
                            <div class="col-6">
                            <label>Job Title</label>
                            <input type="text" v-model="newJob.jobTitle" class="form-control" required>
                            </div>
                            </div>
                        </div>
                    </div>

                    <div style="height: 20px;"></div>
            
                    <!-- dynamic fields -->
                    <div v-for="(step, index) in newJob.steps" :key="index" class="card mb-3">
                        <div class="card-header">
                            <h5 class="mt-1 text-center">Step {{ index + 1 }} Attributes</h5>
                        </div>
                        <div class="card-body">
                            <div class="form-group">
                                <label>Description</label>
                                <textarea v-model="step.description" class="form-control" rows="3" required></textarea>
                            </div>
                            <div class="form-group">
                                <label>Hazards</label>
                                <textarea v-model="step.hazards" class="form-control" rows="3" required></textarea>
                            </div>
                            <div class="form-group">
                                <label>Mitigation</label>
                                <textarea v-model="step.mitigation" class="form-control" rows="3" required></textarea>
                            </div>

                            <br>

                            <button type="button" class="btn btn-danger" @click="removeStep(index)">Remove Step</button>
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
                <div class="container">
                    <h2 class="mb-4 text-center">Frequently Asked Questions</h2>
                    <div class="accordion" id="accordionFAQ">
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="headingOne">
                            <button class="accordion-button collapsed fw-semibold fs-5" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
                                What is a Job Hazard Analysis (JHA)?
                            </button>
                            </h2>
                            <div id="collapseOne" class="accordion-collapse collapse" aria-labelledby="headingOne" data-bs-parent="#accordionFAQ">
                                <div class="accordion-body fs-6">
                                    A JHA is a method for identifying and evaluating hazards associated with tasks (steps) with a specific job or activity and eliminating or mitigating them prior to conducting work.
                                </div>
                            </div>
                        </div>

                        <div class="accordion-item">
                            <h2 class="accordion-header" id="headingTwo">
                            <button class="accordion-button collapsed fw-semibold fs-5" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                                What are the steps in completing a JHA?
                            </button>
                            </h2>
                            <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#accordionFAQ">
                                <div class="accordion-body fs-6">
                                    <p>1. Select the job/activity to be analyzed.</p>
                                    <p>2. Break the job/activity down into a series of tasks.</p>
                                    <p>3. Identify potential hazards and consequences in each task.</p>
                                    <p>4. Determine preventive measures to overcome these hazards.</p>
                                </div>
                            </div>
                        </div>

                        <div class="accordion-item">
                            <h2 class="accordion-header" id="headingThree">
                            <button class="accordion-button collapsed fw-semibold fs-5" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                                Who should conduct a JHA? 
                            </button>
                            </h2>
                            <div id="collapseThree" class="accordion-collapse collapse" aria-labelledby="headingThree" data-bs-parent="#accordionFAQ">
                                <div class="accordion-body fs-6">
                                    Individuals who perform the tasks that are being evaluated should always conduct a JHA.
                                </div>
                            </div>
                        </div>

                        <div class="accordion-item">
                            <h2 class="accordion-header" id="headingFour">
                            <button class="accordion-button collapsed fw-semibold fs-5" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFour" aria-expanded="false" aria-controls="collapseFour">
                                Why conduct a JHA?  
                            </button>
                            </h2>
                            <div id="collapseFour" class="accordion-collapse collapse" aria-labelledby="headingFour" data-bs-parent="#accordionFAQ">
                                <div class="accordion-body fs-6">
                                    A JHA can prevent work-related injuries or illnesses by eliminating or controlling identified hazards. It is a means to ensure that workers have the training, equipment, and supplies to do their jobs safely.
                                </div>
                            </div>
                        </div>

                        <div class="accordion-item">
                            <h2 class="accordion-header" id="headingFive">
                            <button class="accordion-button collapsed fw-semibold fs-5" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFive" aria-expanded="false" aria-controls="collapseFive">
                                What do I do when the JHA is completed?
                            </button>
                            </h2>
                            <div id="collapseFive" class="accordion-collapse collapse" aria-labelledby="headingFive" data-bs-parent="#accordionFAQ">
                                <div class="accordion-body fs-6">
                                    <p>1. Ensure equipment and supplies are acquired to perform the job/activity according to the JHA.</p>
                                    <p>2. Train workers in the procedures, controls, and PPE according to the JHA.</p>
                                    <p>3. Review the JHA periodically and update it when the job/activity or equipment changes. Revise JHA as needed and retrain employees on the revised JHA.</p>
                                    <p>4. Consult your administrative unit to review JHAs as needed.</p> 
                                </div>  
                            </div>
                        </div>

                        <div class="accordion-item">
                            <h2 class="accordion-header" id="headingSix">
                            <button class="accordion-button collapsed fw-semibold fs-5" type="button" data-bs-toggle="collapse" data-bs-target="#collapseSix" aria-expanded="false" aria-controls="collapseSix">
                                Other Information
                            </button>
                            </h2>
                            <div id="collapseSix" class="accordion-collapse collapse" aria-labelledby="headingSix" data-bs-parent="#accordionFAQ">
                                <div class="accordion-body fs-6">
                                    <p>The information in this FAQ section was obtained from the University of Washington's Environmental Health & Safety administrative unit (EH&S). More information regarding JHA's are available at the link below:</p>
                                    <p><a class="link-opacity-100" href="https://www.ehs.washington.edu/workplace/job-hazard-analysis">Job Hazard Analysis | EHS</a></p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-6">
                <!-- submitted jobs -->
                <div class="mx-2 text-center">
                    <h2 class="my-3 mb-4">Submitted JHA's</h2>
                    <div v-for="(job, index) in jobs" :key="index" class="card mb-3">
                        <div class="card-header">
                            <h4 class="mt-1">{{ job.jobTitle }}</h4>
                            <h6>Submitted by {{ job.name }}</h6>
                            <button class="btn btn-sm btn-primary me-1" @click="editJob(index)">Edit</button>
                            <button class="btn btn-sm btn-danger" @click="deleteJob(job.id)">Delete</button>
                        </div>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item" v-for="(step, sIndex) in job.steps" :key="sIndex">
                                <strong>Step {{ sIndex + 1 }}:</strong><br>
                                <strong>Description - </strong> {{ step.description }}<br>
                                <strong>Hazards - </strong> {{ step.hazards }}<br>
                                <strong>Mitigation - </strong> {{ step.mitigation }}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <div style="height: 60px;"></div>
    
  </template>