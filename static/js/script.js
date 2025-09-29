function load_image(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error(`Failed to load image: ${src}`));
    img.src = src;
  });
}

async function load_json(url) {
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(res.status);
    const data = await res.json();
    return data;
  } catch (err) {
    console.error('Fetch error:', err);
  }
}

const canvas = document.getElementById("thumbnail");
const ctx = canvas.getContext("2d");

async function load_assets() {
  try {
    const abyss_12 = await load_image("static/abyss.png");
    const four_star = await load_image("static/4star.png");
    const question = await load_image("static/question.png");
    const epic_fail = await load_image("static/epic_fail.png");
    const chars = await load_json("static/chars.json");
    return { abyss_12, four_star, question, epic_fail, chars };
  } catch (error) {
    console.error("Failed to load assets:", error);
    throw error;
  }
}

const { abyss_12, four_star, question, epic_fail, chars } = await load_assets();

// console.log(chars);

const chars_map = new Map();

for (const item of chars.chars) {
  chars_map.set(item.toLowerCase(), chars.directory + "/" + item + ".png");
}

// console.log(chars_map);

const abyss_label_first = document.getElementById("abyss_label_first");
const abyss_label_second = document.getElementById("abyss_label_second");
const abyss_label_distance = document.getElementById("abyss_label_distance");
const abyss_label_distance_value = document.getElementById("abyss_label_distance_value");
abyss_label_distance_value.textContent = abyss_label_distance.value;

const paste_area_left = document.getElementById('paste_area_left');
const file_input_left = document.getElementById('file_input_left');
const paste_area_right = document.getElementById('paste_area_right');
const file_input_right = document.getElementById('file_input_right');

const background_left_shift = document.getElementById("background_left_shift");
const background_left_shift_value = document.getElementById("background_left_shift_value");
background_left_shift_value.textContent = background_left_shift.value;

const background_right_shift = document.getElementById("background_right_shift");
const background_right_shift_value = document.getElementById("background_right_shift_value");
background_right_shift_value.textContent = background_right_shift.value;

const background_blend = document.getElementById("background_blend");
const background_blend_value = document.getElementById("background_blend_value");
background_blend_value.textContent = background_blend.value;

let background_left;
let background_right;

let left_char1;
let left_char2;
let left_char3;

let right_char1;
let right_char2;
let right_char3;

paste_area_left.addEventListener('paste', (event) => {
  background_left = handle_paste(event);
});
file_input_left.addEventListener('change', (event) => {
  background_left = handle_file_select(event);
});

paste_area_right.addEventListener('paste', (event) => {
  background_right = handle_paste(event);
});
file_input_right.addEventListener('change', (event) => {
  background_right = handle_file_select(event);
});

function handle_paste(event) {
  // Get clipboard data
  const clipboardData = event.clipboardData || window.clipboardData;

  if (!clipboardData) {
    alert('Clipboard API not supported in this browser');
    return;
  }

  // Check if there are image items in clipboard
  if (clipboardData.items) {
    for (let i = 0; i < clipboardData.items.length; i++) {
      if (clipboardData.items[i].type.indexOf('image') !== -1) {
        const blob = clipboardData.items[i].getAsFile();
        let result = process_image_blob(blob);
        event.preventDefault();
        return result;
      }
    }
  }

  alert('No image found in clipboard');
}

function handle_file_select(event) {
  const file = event.target.files[0];
  if (file && file.type.indexOf('image') !== -1) {
    return process_image_blob(file);
  } else {
    alert('Please select a valid image file');
  }
}

function process_image_blob(blob) {
  // Create URL from blob
  const imageUrl = URL.createObjectURL(blob);

  const image = new Image();

  image.onload = function () {
    // Clean up
    URL.revokeObjectURL(imageUrl);
    draw_thumbnail();
  };

  image.onerror = function () {
    alert('Error loading image');
    URL.revokeObjectURL(imageUrl);
  };

  image.src = imageUrl;

  return image;
}

const four_star_checkbox = document.querySelector('#four_star');
const question_checkbox = document.querySelector('#question');
const epic_fail_checkbox = document.querySelector('#epic_fail');

function draw_thumbnail() {
  // console.log("draw_thumbnail");

  ctx.fillStyle = "#888888";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const px = 633;
  const py = 98;
  const shift_left = -parseInt(background_left_shift.value, 10);
  const shift_right = -parseInt(background_right_shift.value, 10);
  const blend = parseInt(background_blend_value.value, 10);

  const mid = 640;
  // const w = 1280;
  const h = 720;

  if (background_left && background_right && blend > 0) {
    ctx.drawImage(background_left,
      px + shift_left, py, mid + blend, h,
      0, 0, mid + blend, h);

    const off = document.createElement('canvas');
    off.width = blend * 2;
    off.height = h;
    const octx = off.getContext('2d');

    octx.drawImage(background_right,
      px + shift_right - blend, py, blend * 2, h,
      0, 0, blend * 2, h);

    const grad = octx.createLinearGradient(0, 0, blend * 2, 0);
    grad.addColorStop(0, 'rgba(0,0,0,0)');
    grad.addColorStop(1, 'rgba(0,0,0,1)');

    octx.globalCompositeOperation = 'destination-in';
    octx.fillStyle = grad;
    octx.fillRect(0, 0, blend * 2, h);

    ctx.drawImage(off, mid - blend, 0);

    if (background_right) {
      ctx.drawImage(background_right,
        px + shift_right + blend, py, mid - blend, h,
        mid + blend, 0, mid - blend, h);
    }

  } else {
    if (background_left) {
      ctx.drawImage(background_left,
        px + shift_left, py, mid, h,
        0, 0, mid, h);
    }

    if (background_right) {
      ctx.drawImage(background_right,
        px + shift_right, py, mid, h,
        mid, 0, mid, h);
    }
  }

  ctx.drawImage(abyss_12, 0, 0);

  ctx.font = "bold 100px Arial";

  // Set outline style
  ctx.strokeStyle = "#431700";
  ctx.lineWidth = 25;
  ctx.lineJoin = "round";
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  const fist_line = abyss_label_first.value;
  const second_line = abyss_label_second.value;

  const text_distance = parseInt(abyss_label_distance.value, 10);

  ctx.strokeText(fist_line, 640, 360 - text_distance);
  ctx.strokeText(second_line, 640, 360 + text_distance);

  ctx.fillStyle = "#ffe74e";

  ctx.fillText(fist_line, 640, 360 - text_distance);
  ctx.fillText(second_line, 640, 360 + text_distance);

  if (left_char1) {
    ctx.drawImage(left_char1, 0, 0, left_char1.width, left_char1.height, 0, 50, 200, 200);
  }

  if (left_char2) {
    ctx.drawImage(left_char2, 0, 0, left_char2.width, left_char2.height, 0, 260, 200, 200);
  }

  if (left_char3) {
    ctx.drawImage(left_char3, 0, 0, left_char3.width, left_char3.height, 0, 470, 200, 200);
  }

  if (right_char1) {
    ctx.drawImage(right_char1, 0, 0, right_char1.width, right_char1.height, 1080, 50, 200, 200);
  }

  if (right_char2) {
    ctx.drawImage(right_char2, 0, 0, right_char2.width, right_char2.height, 1080, 260, 200, 200);
  }

  if (right_char3) {
    ctx.drawImage(right_char3, 0, 0, right_char3.width, right_char3.height, 1080, 470, 200, 200);
  }

  // extra 
  if (four_star_checkbox.checked) {
    ctx.drawImage(four_star, 0, 0);
  }
  if (question_checkbox.checked) {
    ctx.drawImage(question, 0, 0);
  }
  if (epic_fail_checkbox.checked) {
    ctx.drawImage(epic_fail, 0, 0);
  }
}

abyss_label_first.addEventListener("input", (event) => {
  draw_thumbnail();
});

abyss_label_second.addEventListener("input", (event) => {
  draw_thumbnail();
});

abyss_label_distance.addEventListener("input", (event) => {
  abyss_label_distance_value.textContent = abyss_label_distance.value;
  draw_thumbnail();
});

background_left_shift.addEventListener("input", (event) => {
  background_left_shift_value.textContent = background_left_shift.value;
  draw_thumbnail();
});

background_right_shift.addEventListener("input", (event) => {
  background_right_shift_value.textContent = background_right_shift.value;
  draw_thumbnail();
});

background_blend.addEventListener("input", (event) => {
  background_blend_value.textContent = background_blend.value;
  draw_thumbnail();
});


four_star_checkbox.addEventListener("input", (event) => {
  draw_thumbnail();
});
question_checkbox.addEventListener("input", (event) => {
  draw_thumbnail();
});
epic_fail_checkbox.addEventListener("input", (event) => {
  draw_thumbnail();
});

draw_thumbnail();

const first_team1 = document.getElementById('first_team1')
const first_team2 = document.getElementById('first_team2')
const first_team3 = document.getElementById('first_team3')

const second_team1 = document.getElementById('second_team1')
const second_team2 = document.getElementById('second_team2')
const second_team3 = document.getElementById('second_team3')

// I hate this T_T

function auto_cfg() {
  return {
    autoFirst: true,
    list: chars.chars
  };
}

new Awesomplete(first_team1, auto_cfg());
new Awesomplete(first_team2, auto_cfg());
new Awesomplete(first_team3, auto_cfg());
new Awesomplete(second_team1, auto_cfg());
new Awesomplete(second_team2, auto_cfg());
new Awesomplete(second_team3, auto_cfg());

// 1 char

function handle_char1(event) {
  const actual_value = first_team1.value.toLowerCase();
  if (chars_map.has(actual_value)) {
    left_char1 = new Image;
    left_char1.onload = function () {
      draw_thumbnail();
    };
    left_char1.src = chars_map.get(actual_value);
  } else {
    left_char1 = undefined;
    draw_thumbnail();
  }
}

first_team1.addEventListener("input", (event) => {
  handle_char1();
});

first_team1.addEventListener('awesomplete-selectcomplete', event => {
  handle_char1();
});

// 2 char

function handle_char2(event) {
  const actual_value = first_team2.value.toLowerCase();
  if (chars_map.has(actual_value)) {
    left_char2 = new Image;
    left_char2.onload = function () {
      draw_thumbnail();
    };
    left_char2.src = chars_map.get(actual_value);
  } else {
    left_char2 = undefined;
    draw_thumbnail();
  }
}

first_team2.addEventListener("input", (event) => {
  handle_char2();
});

first_team2.addEventListener('awesomplete-selectcomplete', event => {
  handle_char2();
});

// 3 char

function handle_char3(event) {
  const actual_value = first_team3.value.toLowerCase();
  if (chars_map.has(actual_value)) {
    left_char3 = new Image;
    left_char3.onload = function () {
      draw_thumbnail();
    };
    left_char3.src = chars_map.get(actual_value);
  } else {
    left_char3 = undefined;
    draw_thumbnail();
  }
}

first_team3.addEventListener("input", (event) => {
  handle_char3();
});

first_team3.addEventListener('awesomplete-selectcomplete', event => {
  handle_char3();
});

// 4 char

function handle_char4(event) {
  const actual_value = second_team1.value.toLowerCase();
  if (chars_map.has(actual_value)) {
    right_char1 = new Image;
    right_char1.onload = function () {
      draw_thumbnail();
    };
    right_char1.src = chars_map.get(actual_value);
  } else {
    right_char1 = undefined;
    draw_thumbnail();
  }
}

second_team1.addEventListener("input", (event) => {
  handle_char4();
});

second_team1.addEventListener('awesomplete-selectcomplete', event => {
  handle_char4();
});

// 5 char

function handle_char5(event) {
  const actual_value = second_team2.value.toLowerCase();
  if (chars_map.has(actual_value)) {
    right_char2 = new Image;
    right_char2.onload = function () {
      draw_thumbnail();
    };
    right_char2.src = chars_map.get(actual_value);
  } else {
    right_char2 = undefined;
    draw_thumbnail();
  }
}

second_team2.addEventListener("input", (event) => {
  handle_char5();
});

second_team2.addEventListener('awesomplete-selectcomplete', event => {
  handle_char5();
});

// 6 char

function handle_char6(event) {
  const actual_value = second_team3.value.toLowerCase();
  if (chars_map.has(actual_value)) {
    right_char3 = new Image;
    right_char3.onload = function () {
      draw_thumbnail();
    };
    right_char3.src = chars_map.get(actual_value);
  } else {
    right_char3 = undefined;
    draw_thumbnail();
  }
}

second_team3.addEventListener("input", (event) => {
  handle_char6();
});

second_team3.addEventListener('awesomplete-selectcomplete', event => {
  handle_char6();
});
