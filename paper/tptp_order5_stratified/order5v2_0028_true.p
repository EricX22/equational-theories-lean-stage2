% order5v2_0028  eq1=36879 eq2=27096  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),Y),f(Y,W)),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(Y,Y),f(Z,Z)),f(W,Z)) )).
