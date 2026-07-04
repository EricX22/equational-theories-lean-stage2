% order5v2_1233  eq1=38360 eq2=45245  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,f(f(X,Z),W)),Z),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(f(f(X,X),Y),Z)) )).
