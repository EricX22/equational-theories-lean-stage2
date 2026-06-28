% hard3_0116  eq1=930 eq2=2998  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Y,Z),f(Y,X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,f(Z,Y)),Z),X) )).
