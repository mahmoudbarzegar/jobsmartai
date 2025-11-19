/*!

=========================================================
* Argon Dashboard React - v1.2.4
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-dashboard-react
* Copyright 2024 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
// reactstrap components
import React, { useEffect, useState } from "react";

import {
  Card,
  CardHeader,
  DropdownMenu,
  DropdownItem,
  UncontrolledDropdown,
  DropdownToggle,
  Table,
  Container,
  Row,
  Button,
  Modal,
  ModalBody,
  ModalFooter,
} from "reactstrap";
// core components
import Header from "components/Headers/Header";

interface Job {
  id: number;
  title: string;
  description: string;
  cover_letter?: string;
  score?: string;
  resume_url: string;
}
interface JobDetail {
  title: string;
  detail?: string;
}
interface Resume {
  id: number;
  file?: string;
}

const Jobs = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedJob, setSelectedJob] = useState<JobDetail>();
  const [jobDetailModalOpen, setJobDetailModalOpen] = React.useState(false);
  const [jobAddModalOpen, setJobAddModalOpen] = useState(false);
  const [resumes, setResumes] = useState<Resume[]>([]);

  const [newJob, setNewJob] = useState({
    title: "",
    description: "",
    resume_id: "",
  });
  const handleViewJobDetail = (title: string, detail: string | undefined) => {
    setJobDetailModalOpen(!jobDetailModalOpen);
    setSelectedJob({
      title: title,
      detail: detail,
    });
  };

  const handleAddJob = (e: object) => {
    setJobAddModalOpen(!jobAddModalOpen);
  };

  // Add this handler function
  const handleInputChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    const { name, value } = e.target;
    setNewJob((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Add this submit handler
  const handleSubmitJob = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:8000/api/jobs", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newJob),
      });

      if (response.ok) {
        const data = await response.json();
        // Refresh the jobs list
        setJobs([data.result, ...jobs]);
        // Close modal and reset form
        setJobAddModalOpen(false);
        setNewJob({ title: "", description: "", resume_id: "" });
      }
    } catch (error) {
      console.error("Error adding job:", error);
    }
  };

  useEffect(() => {
    setLoading(true);
    fetch("http://localhost:8000/api/jobs")
      .then((res) => res.json())
      .then((data) => {
        setJobs(data.result.data);
        setLoading(false);
      })
      .catch((err) => console.error("Error fetching resumes:", err));
  }, []);

  // Fetch resumes when component mounts (add to existing useEffect or create new one)
  useEffect(() => {
    fetch("http://localhost:8000/api/resumes")
      .then((res) => res.json())
      .then((data) => {
        setResumes(data.result.data); // Adjust based on your API response structure
      })
      .catch((err) => console.error("Error fetching resumes:", err));
  }, []);

  console.log(jobs);
  return (
    <>
      <Header />
      {/* Page content */}
      <Container className="mt--7" fluid>
        <Row className="mt-5">
          <div className="col">
            <Card className="shadow">
              <CardHeader className="bg-transparent border-0">
                <div className="col-12">
                  <Button
                    color="info"
                    type="button"
                    onClick={(e) => handleAddJob(e)}
                  >
                    Add Job
                  </Button>
                </div>
              </CardHeader>
              <Table className="align-items-center table-flush" responsive>
                <thead className="thead-black">
                  <tr>
                    <th scope="col">Job Name</th>
                    <th scope="col">Score</th>
                    <th scope="col">Resume</th>
                    <th scope="col" />
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr>
                      <td colSpan={4} className="text-center py-4">
                        <div className="d-flex justify-content-center align-items-center">
                          <span className="fa fa-spinner fa-spin fa-2x text-primary" />
                        </div>
                      </td>
                    </tr>
                  ) : (
                    jobs.map((job) => (
                      <tr key={job.id}>
                        <th scope="row">
                          <span
                            className="mb-0 text-sm text-truncate d-inline-block job-title-hover"
                            title={job?.title}
                          >
                            {" "}
                            {job?.title?.length > 35
                              ? job?.title?.substring(0, 35) + "..."
                              : job?.title}
                          </span>
                        </th>
                        <th scope="col">
                          {job?.score ? (
                            job?.score
                          ) : (
                            <Button color="info" type="button">
                              Get core
                            </Button>
                          )}
                        </th>
                        <td>
                          <a href={job?.resume_url} target="_blank">
                            View
                          </a>
                        </td>
                        <td className="text-right">
                          <UncontrolledDropdown>
                            <DropdownToggle
                              className="btn-icon-only text-black"
                              href="#pablo"
                              role="button"
                              size="sm"
                              color=""
                              onClick={(e) => e.preventDefault()}
                            >
                              <i className="fas fa-ellipsis-v" />
                            </DropdownToggle>
                            <DropdownMenu className="dropdown-menu-arrow" right>
                              <DropdownItem
                                href="#pablo"
                                onClick={() =>
                                  handleViewJobDetail(
                                    job.title,
                                    job.cover_letter
                                  )
                                }
                              >
                                View Cover Letter
                              </DropdownItem>
                              <DropdownItem
                                href="#pablo"
                                onClick={() =>
                                  handleViewJobDetail(
                                    job.title,
                                    job.description
                                  )
                                }
                              >
                                View Job Detail
                              </DropdownItem>
                            </DropdownMenu>
                          </UncontrolledDropdown>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </Table>
            </Card>
          </div>
        </Row>

        <Modal
          toggle={() => setJobDetailModalOpen(!jobDetailModalOpen)}
          isOpen={jobDetailModalOpen}
        >
          <div className=" modal-header">
            <h5 className=" modal-title" id="exampleModalLabel">
              {selectedJob?.title}
            </h5>
            <button
              aria-label="Close"
              className=" close"
              type="button"
              onClick={() => setJobDetailModalOpen(!jobDetailModalOpen)}
            >
              <span aria-hidden={true}>×</span>
            </button>
          </div>
          <ModalBody>
            <pre style={{ whiteSpace: "pre-wrap", fontFamily: "inherit" }}>
              {selectedJob?.detail}
            </pre>
          </ModalBody>
          <ModalFooter>
            <Button
              color="secondary"
              type="button"
              onClick={() => setJobDetailModalOpen(!jobDetailModalOpen)}
            >
              Close
            </Button>
          </ModalFooter>
        </Modal>
        <Modal
          toggle={() => setJobAddModalOpen(!jobAddModalOpen)}
          isOpen={jobAddModalOpen}
        >
          <div className="modal-header">
            <h5 className="modal-title" id="exampleModalLabel">
              Add a New Job
            </h5>
            <button
              aria-label="Close"
              className="close"
              type="button"
              onClick={() => setJobAddModalOpen(!jobAddModalOpen)}
            >
              <span aria-hidden={true}>×</span>
            </button>
          </div>
          <form onSubmit={handleSubmitJob}>
            <ModalBody>
              <div className="form-group">
                <label htmlFor="jobTitle" className="form-label">
                  Job Title <span className="text-danger">*</span>
                </label>
                <input
                  type="text"
                  id="jobTitle"
                  name="title"
                  className="form-control"
                  placeholder="e.g. Backend Software Engineer"
                  value={newJob.title}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="jobDescription" className="form-label">
                  Job Description <span className="text-danger">*</span>
                </label>
                <textarea
                  id="jobDescription"
                  name="description"
                  className="form-control"
                  rows={6}
                  placeholder="Paste the job description here..."
                  value={newJob.description}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="resumeSelect" className="form-label">
                  Select Resume <span className="text-danger">*</span>
                </label>
                <select
                  id="resumeSelect"
                  name="resume_id"
                  className="form-control"
                  value={newJob.resume_id}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">-- Select a Resume --</option>
                  {resumes.map((resume) => (
                    <option key={resume.id} value={resume.id}>
                      {resume.file}
                    </option>
                  ))}
                </select>
              </div>
            </ModalBody>
            <ModalFooter>
              <Button
                color="secondary"
                type="button"
                onClick={() => {
                  setJobAddModalOpen(false);
                  setNewJob({ title: "", description: "", resume_id: "" });
                }}
              >
                Cancel
              </Button>
              <Button color="primary" type="submit">
                Add Job
              </Button>
            </ModalFooter>
          </form>
        </Modal>
      </Container>
    </>
  );
};

export default Jobs;
