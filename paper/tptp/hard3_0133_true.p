% hard3_0133  eq1=1054 eq2=2264  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(X,f(f(Y,f(Y,Z)),W)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(X,f(Y,f(Y,X))),Y) )).
