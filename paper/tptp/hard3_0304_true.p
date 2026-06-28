% hard3_0304  eq1=2859 eq2=1647  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(X,f(X,Y)),Z),Y) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(X,Y),f(f(X,Y),X)) )).
