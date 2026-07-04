% order5v2_1385  eq1=25732 eq2=36315  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(Y,f(Z,f(W,U))),f(U,Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(f(X,X),Y),f(Z,W)),Y) )).
