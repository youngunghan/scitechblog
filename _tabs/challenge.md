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
  background: linear-gradient(135deg, #1f5f68 0%, #173f46 100%);
  color: white;
  padding: 15px 20px;
  cursor: pointer;
  font-weight: 600;
  font-size: 16px;
  list-style: none;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.25s ease;
  user-select: none;
}

details.course-item summary:hover {
  background: linear-gradient(135deg, #26707a 0%, #1d525b 100%);
  transform: translateX(3px);
}

details.course-item.completed summary {
  background: linear-gradient(135deg, #1f5f68 0%, #173f46 100%);
}

details.course-item.in-progress summary {
  background: linear-gradient(135deg, #9a5f12 0%, #70430c 100%);
}

details.course-item.not-started summary {
  background: linear-gradient(135deg, #45535c 0%, #313b42 100%);
}

details.course-item summary::-webkit-details-marker {
  display: none;
}

.course-toggle {
  font-size: 20px;
  transition: transform 0.25s ease;
  display: inline-block;
  width: 20px;
  flex: 0 0 20px;
}

.course-title {
  min-width: 0;
  flex: 1 1 auto;
}

details[open] .course-toggle {
  transform: rotate(90deg);
}

.course-status {
  flex: 0 0 auto;
  font-size: 13px;
  background: rgba(255, 255, 255, 0.18);
  padding: 4px 12px;
  border-radius: 12px;
  white-space: nowrap;
}

.course-content {
  background: #f5f7f9;
  border: 1px solid #d8dee4;
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
  border-bottom: 1px solid #d8dee4;
}

.course-content li:last-child {
  border-bottom: none;
}

.course-content strong {
  color: #1f5f68;
  display: inline-block;
  min-width: 120px;
}

.rating-badge {
  background: #1f5f68;
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
    <span class="course-title">M1407.001200: Mathematical Foundations of Deep Neural Networks</span>
    <span class="course-status">IN PROGRESS</span>
  </summary>
  <div class="course-content">
    <ul>
      <li><strong>University:</strong> Seoul National University (서울대학교)</li>
      <li><strong>Semester:</strong> Spring 2024</li>
      <li><strong>Instructor:</strong> Ernest Ryu</li>
      <li><strong>Course Page:</strong> <a href="https://ernestryu.com/courses/deep_learning.html" target="_blank">Course Website</a></li>
      <li><strong>Assignments:</strong> Google Drive Folder <em>(Coming soon)</em></li>
      <li><strong>Topics:</strong> Neural Networks, Backpropagation, CNNs, RNNs, Transformers</li>
    </ul>
  </div>
</details>

<details class="course-item not-started">
  <summary>
    <span class="course-toggle">▶</span>
    <span class="course-title">EECS 498: Deep Learning for Computer Vision</span>
    <span class="course-status">PLANNED</span>
  </summary>
  <div class="course-content">
    <ul>
      <li><strong>University:</strong> University of Michigan (미시간 대학교)</li>
      <li><strong>Semester:</strong> Fall 2020</li>
      <li><strong>Instructor:</strong> Justin Johnson</li>
      <li><strong>Course Page:</strong> <a href="https://web.eecs.umich.edu/~justincj/teaching/eecs498/FA2020/" target="_blank">EECS 498-007 / 598-005</a></li>
      <li><strong>Video Lectures:</strong> <a href="https://www.youtube.com/playlist?list=PL5-TkQAfAZFbzxjBHtzdVCWE0Zbhomg7r" target="_blank">YouTube Playlist</a></li>
      <li><strong>Assignments:</strong> Google Drive Folder <em>(Coming soon)</em></li>
      <li><strong>Topics:</strong> Image Classification, Object Detection, Segmentation, GANs, 3D Vision</li>
    </ul>
  </div>
</details>
