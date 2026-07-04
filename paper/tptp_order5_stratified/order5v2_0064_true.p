% order5v2_0064  eq1=39616 eq2=4658  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),f(Z,W)),Y),W) )).
fof(goal, conjecture, ! [X,Y] : ( f(f(X,Y),Y) = f(f(Y,X),X) )).
