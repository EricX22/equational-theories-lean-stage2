% hard3_0149  eq1=1232 eq2=3740  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(X,f(f(f(X,Y),Y),Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(X,Z),f(Z,Y)) )).
