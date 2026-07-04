% order5_0213  eq1=1422 eq2=22163  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(f(f(Z,W),U),Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,W)),f(Z,f(W,Z))) )).
