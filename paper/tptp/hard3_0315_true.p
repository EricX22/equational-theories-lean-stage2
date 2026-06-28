% hard3_0315  eq1=2927 eq2=765  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,f(X,Z)),Z),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(Z,f(f(Y,Z),X))) )).
