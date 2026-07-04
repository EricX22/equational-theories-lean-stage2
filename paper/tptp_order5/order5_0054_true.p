% order5_0054  eq1=2150 eq2=32872  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,Y),Z),f(Y,Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,f(f(f(Y,Y),Z),Y)),X) )).
