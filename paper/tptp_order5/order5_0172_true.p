% order5_0172  eq1=22261 eq2=3915  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(X,f(X,Y)),f(f(Y,X),Y)) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(f(X,f(X,X)),Y) )).
