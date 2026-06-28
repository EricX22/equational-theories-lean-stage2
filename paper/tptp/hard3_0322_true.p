% hard3_0322  eq1=2998 eq2=3870  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,f(Z,Y)),Z),X) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(f(X,f(Y,Y)),X) )).
