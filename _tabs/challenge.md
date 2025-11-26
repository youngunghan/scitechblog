---
icon: fas fa-trophy
order: 2
---

# AI Challenge

Inspired by [Scott Young's MIT Challenge](https://www.scotthyoung.com/blog/myprojects/mit-challenge-2/)

---

<style>
details.course-item {
  margin-bottom: 10px;
  border-radius: 8px;
  overflow: hidden;
}

details.course-item summary {
  background: linear-gradient(135deg, #2d9da8 0%, #2d8a9a 100%);
  color: white;
  padding: 15px 20px;
  cursor: pointer;
  font-weight: 600;
  font-size: 16px;
  list-style: none;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
  user-select: none;
}

details.course-item summary:hover {
  background: linear-gradient(135deg, #3ab0bd 0%, #359faf 100%);
  transform: translateX(5px);
}

details.course-item.completed summary {
  background: linear-gradient(135deg, #2d9da8 0%, #2d8a9a 100%);
}

details.course-item.in-progress summary {
  background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%);
}

details.course-item.not-started summary {
  background: linear-gradient(135deg, #78909c 0%, #546e7a 100%);
}

details.course-item summary::-webkit-details-marker {
  display: none;
}

.course-toggle {
  margin-right: 10px;
  font-size: 20px;
  transition: transform 0.3s ease;
  display: inline-block;
  width: 20px;
}

details[open] .course-toggle {
  transform: rotate(90deg);
}

.course-status {
  margin-left: auto;
  font-size: 14px;
  background: rgba(255,255,255,0.2);
  padding: 4px 12px;
  border-radius: 12px;
}

.course-content {
  background: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-top: none;
  padding: 20px;
}

.course-content ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
}

.course-content li {
  padding: 8px 0;
  border-bottom: 1px solid #e0e0e0;
}

.course-content li:last-child {
  border-bottom: none;
}

.course-content strong {
  color: #2d9da8;
  display: inline-block;
  min-width: 120px;
}

.rating-badge {
  background: #2d9da8;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  margin-left: 10px;
}
</style>

<details class="course-item in-progress">
  <summary>
    <span class="course-toggle">▶</span>
    <span>Mathematical Foundations of Deep Neural Networks</span>
    <span class="course-status">IN PROGRESS</span>
  </summary>
  <div class="course-content">
    <ul>
      <li><strong>University:</strong> Seoul National University (서울대학교)</li>
      <li><strong>Semester:</strong> Spring 2024</li>
      <li><strong>Instructor:</strong> Ernest Ryu</li>
      <li><strong>Course Page:</strong> <a href="https://ernestryu.com/courses/deep_learning.html" target="_blank">Course Website</a></li>
      <li><strong>Assignments:</strong> <a href="#" target="_blank">Google Drive Folder</a> <em>(Coming soon)</em></li>
      <li><strong>Topics:</strong> Neural Networks, Backpropagation, CNNs, RNNs, Transformers</li>
    </ul>
  </div>
</details>

<details class="course-item not-started">
  <summary>
    <span class="course-toggle">▶</span>
    <span>EECS 498: Deep Learning for Computer Vision</span>
    <span class="course-status">PLANNED</span>
  </summary>
  <div class="course-content">
    <ul>
      <li><strong>University:</strong> University of Michigan (미시간 대학교)</li>
      <li><strong>Semester:</strong> Fall 2020</li>
      <li><strong>Instructor:</strong> Justin Johnson</li>
      <li><strong>Course Page:</strong> <a href="https://web.eecs.umich.edu/~justincj/teaching/eecs498/FA2020/" target="_blank">EECS 498-007 / 598-005</a></li>
      <li><strong>Video Lectures:</strong> <a href="https://www.youtube.com/playlist?list=PL5-TkQAfAZFbzxjBHtzdVCWE0Zbhomg7r" target="_blank">YouTube Playlist</a></li>
      <li><strong>Assignments:</strong> <a href="#" target="_blank">Google Drive Folder</a> <em>(Coming soon)</em></li>
      <li><strong>Topics:</strong> Image Classification, Object Detection, Segmentation, GANs, 3D Vision</li>
    </ul>
  </div>
</details>
