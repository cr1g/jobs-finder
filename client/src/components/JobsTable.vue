<template>
    <div class="overflow-auto">
        <b-table
                id="my-table"
                :items="filteredJobs"
                :fields="fields"
                :per-page="perPage"
                :current-page="currentPage"
                small
                responsive
        >
            <template slot="name" slot-scope="row">
                <a href="#" @click="changeStatus(row.item)" @click.middle="changeStatus(row.item)">{{row.item.name}}</a>
            </template>
            <template slot="status" slot-scope="row">
                <i v-if="row.value === 'seen'" class="fa fa-eye seen" v-b-tooltip.hover title="Seen"></i>
                <i v-else class="fa fa-eye unseen" v-b-tooltip.hover title="Unseen"></i>
            </template>
            <template slot="favourite" slot-scope="row">
                <i @click="updateFavourite(row.item)" v-if="row.value === 1" class="fas fa-star"></i>
                <i @click="updateFavourite(row.item)" v-else class="far fa-star"></i>
            </template>
        </b-table>

        <b-pagination
                v-model="currentPage"
                :total-rows="rows" target=""
                :per-page="perPage"
                aria-controls="my-table"
                align="center"
        ></b-pagination>
    </div>
</template>

<script>
    import {bus} from "../main"

    export default {
        name: "JobsTable",
        data() {
            return {
                jobs: [],
                filteredJobs: [],
                perPage: 10,
                currentPage: 1,
                fields: {
                    name: {
                        "label": "Name"
                    },
                    status: {
                        "label": "Status"
                    },
                    favourite: {
                        "label": "Favourite"
                    }
                }
            }
        },
        mounted() {
            fetch(`http://localhost:5050/jobs`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(response => response.json())
                .then(res => {
                    res.forEach((job) => {
                        this.jobs.push({
                            "name": job['name'],
                            "link": job['link'],
                            "job_id": job['job_id'],
                            "status": job['status'],
                            "favourite": job['favourite']
                        })
                    })
                    this.filteredJobs = this.jobs
                });

            bus.$on("filterJobsEvent", (data) => {
                if(data['key'] === 'all') {
                    this.filteredJobs = this.jobs
                } else {
                    this.filterJobs(this.jobs, data)
                }
            })
        },
        methods: {
            changeStatus(job) {
                window.open(job.link, "_blank")
                fetch(`http://localhost:5050/jobs/${job.job_id}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({"status": "seen"})
                });
                job.status = "seen"
            },
            updateFavourite(job) {
                fetch(`http://localhost:5050/jobs/${job.job_id}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({"favourite": !job.favourite ? 1 : 0})
                });

                job.favourite = !job.favourite ? 1 : 0
            },
            filterJobs(jobs, filter) {
                this.filteredJobs = []

                this.jobs.forEach((job) => {
                    if (job[filter['key']] === filter['value']) {
                        this.filteredJobs.push(job)
                    }
                })
            }
        },
        computed: {
            rows() {
                return this.filteredJobs.length
            }
        }
    }
</script>

<style scoped>
    .seen {
        color: limegreen;
    }

    .unseen {
        color: gray
    }

    .fa-star {
        color: #FBC02D;
        cursor: pointer;
    }

    [class^="icon-"], [class*=" icon-"] {
        display: inline-block;
        width: 100%;
        text-align: center;
    }
</style>
