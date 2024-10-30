from pico2d import load_image, get_time
from state_machine import StateMachine, time_out, space_down, right_down, left_down, left_up, right_up, start_event

class Boy:
  def __init__(self):
    self.x, self.y = 400, 90
    self.frame = 0
    self.action = 3
    self.image = load_image('animation_sheet.png')
    self.state_machine = StateMachine(self) # Boy 인스턴스들은 각자의 state_machine을 갖는다
    self.state_machine.start(Idle) # 파이썬에서는 클래스 이름을 파라미터로 넘겨줄 수 있다.
    self.state_machine.set_transitions(
      {
        Idle : { right_down : Run, left_down : Run, left_up : Run, right_up : Run, time_out : Sleep }, # key는 cur_state : val은 다시 Dictionary
        Run : {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle}, # Run 상태에서 어떤 이벤트가 들어와도 처리하지 않겠다
        Sleep : { right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down : Idle }
      }
    )

  def update(self):
    self.state_machine.update()

  def handle_event(self, event):
    # event : 입력 이벤트 key, mouse...
    # 우리가 statme_machine에게 전달해줄 것은 ( , ) -> Tuple
    self.state_machine.add_event(
      ('INPUT', event)
    )

  def draw(self):
    # self.image.clip_draw(self.frame*100, self.action*100, 100, 100, self.x, self.y)
    self.state_machine.draw()

# 상태를 클래스를 통해서 정의함.
class Idle:
  # @는 "Decorator"라는 개념. static method는 객체가 실행하는 멤버 함수가 아니라 클래스 안에 있는 객체와 상관없는 함수.
  # 클래스로 함수들을 그룹화하기 위해 사용하는 것.
  @staticmethod
  def enter(boy, e):
    if left_up(e) or right_down(e):
      boy.action = 2
      boy.face_dir = -1
    elif right_up(e) or left_down(e)or start_event(e):
      boy.action = 3
      boy.face_dir = 1

    boy.dir = 0 # 정지 상태
    boy.frame = 0
    boy.start_time = get_time() # 현재 시간을 저장
  @staticmethod
  def exit(boy, e):
    pass
  @staticmethod
  def do(boy):
    boy.frame = (boy.frame+1) % 8
    if get_time() - boy.start_time > 3:
      boy.state_machine.add_event(('TIME_OUT',0)) # 3초 경과 시, 내부 이벤트 발생
  @staticmethod
  def draw(boy):
    boy.image.clip_draw(boy.frame*100, boy.action*100, 100, 100, boy.x, boy.y)

class Sleep:
  @staticmethod
  def enter(boy, e):
    pass
  @staticmethod
  def exit(boy, e):
    pass
  @staticmethod
  def do(boy):
    boy.frame = (boy.frame+1) % 8
    pass
  @staticmethod
  def draw(boy):
    if boy.face_dir == 1:
      boy.image.clip_composite_draw(
        boy.frame*100, 300, 100, 100,
        3.141592/2, # 90도 회전
        ' ', # 좌우상하 반전 X
        boy.x-25, boy.y-35, 100, 100
      )
    elif boy.face_dir == -1:
      boy.image.clip_composite_draw(
        boy.frame * 100, 200, 100, 100,
        -3.141592 / 2,  # 90도 회전
        ' ',  # 좌우상하 반전 X
        boy.x + 25, boy.y - 35, 100, 100
      )
    pass

class Run:
  @staticmethod
  def enter(boy, e):
    if right_down(e) or left_up(e):
      boy.dir = 1 # 오른쪽 방ㅎ량
      boy.action = 1
    elif left_down(e) or right_up(e):
      boy.dir = -1
      boy.action = 0
    boy.frame = 0
    pass
  @staticmethod
  def exit(boy, e):
    pass
  @staticmethod
  def do(boy):
    boy.x += boy.dir*5
    boy.frame = (boy.frame + 1) % 8
    pass
  @staticmethod
  def draw(boy):
    boy.image.clip_draw(
      boy.frame*100, boy.action*100, 100, 100,
      boy.x, boy.y
    )
  pass

class AutoRun:
  @staticmethod
  def enter(boy, e):
    pass
  @staticmethod
  def exit(boy, e):
    pass
  @staticmethod
  def do(boy):
    pass
  @staticmethod
  def draw(boy):
    pass