% order5v2_1890  eq1=36168 eq2=32819  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,W)),f(Y,W)),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,f(f(f(Y,X),X),Z)),Z) )).
