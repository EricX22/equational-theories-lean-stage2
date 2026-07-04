% order5v2_1163  eq1=6826 eq2=39670  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Y,f(f(X,Z),f(X,W)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),f(W,Y)),Z),X) )).
