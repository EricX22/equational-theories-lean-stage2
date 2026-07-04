% order5_0085  eq1=25722 eq2=9102  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(Y,f(Z,f(W,U))),f(Z,U)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(X,f(f(X,Y),f(X,f(Z,Y)))) )).
