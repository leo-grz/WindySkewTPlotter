# TODO List
**For now this project is set on ice.**

## Overview
This document tracks pending tasks, planned improvements, and bug fixes for the project.

## Priorities
- 🟥 **High Priority**: Critical tasks that need immediate attention.
- 🟧 **Medium Priority**: Important tasks that improve functionality or fix issues.
- 🟩 **Low Priority**: Enhancements or nice-to-have features.

---

### 🔧 Current Tasks
#### 🟥 High Priority
- [ ] Fix Skew-T subplot=ax bug

#### 🟧 Medium Priority

#### 🟩 Low Priority

---

### 📝 Planned Features
- [ ] **Calculation of additional weather parameters** like FRZ, MaxT ConvT, additional Hodograph vectors
- [ ] **Implement Metadata readout** of sounding files
- [ ] **Implement config validation** to prevent incorrect settings.
- [ ] **Implement tests** to for data and calculation completeness.
- [ ] **Add mouse interaction** like malr, dalr, mixing ratio (basically live lcl)
- [ ] **Add GUI interface** (either configure buttons in fig or separately)
- [ ] **Add location of sounding** in map form
- [ ] **Report outliers in data** during data validation
- [ ] **Add toggable forecast guidance for parameters** like which range is normal, how to interpret
- [ ] **Implement effective error handeling**
- [ ] **Implement logging**
- [ ] **Improvement of runtime possible?**

---

### 🐛 Known Bugs
- [ ] **Supposed Skew-T does not show skewed plots** when creating the fig and ax objects in main.py. The error lies in the matplotlib creation of the fig and handing it to the SkewT constructor of metpy by handing the matplotlib ax to it using the subplot parameter

---

### 🔮 Future Ideas (Backlog)
- [ ] **Support for new data formats**
- [ ] **Convert to windy.com plugin**
