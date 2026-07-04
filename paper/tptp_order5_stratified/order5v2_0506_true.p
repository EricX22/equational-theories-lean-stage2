% order5v2_0506  eq1=38787 eq2=44246  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,f(f(Z,W),Y)),X),U) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,X) = f(Y,f(f(X,f(Z,W)),Z)) )).
